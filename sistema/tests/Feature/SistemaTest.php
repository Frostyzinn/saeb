<?php

namespace Tests\Feature;

use App\Models\Produto;
use App\Models\Usuario;
use App\Services\OrdenacaoService;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Tests\TestCase;

class SistemaTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        $this->seed();
    }

    private function usuario()
    {
        return Usuario::first();
    }

    private function dados(): array
    {
        return ['nome' => 'Serrote', 'marca' => 'Vonder', 'modelo' => 'S1', 'material' => 'Aço', 'tamanho' => '30 cm', 'peso' => '0.60', 'tensao' => 'Não se aplica', 'estoque' => 10, 'estoque_minimo' => 2];
    }

    private function movimento(array $dados = []): array
    {
        return array_merge(['produto_id' => 1, 'tipo' => 'entrada', 'quantidade' => 3, 'data_movimentacao' => now()->toDateString()], $dados);
    }

    public function test_login_com_sucesso(): void
    {
        $this->post('/login', ['email' => 'admin@teste.com', 'password' => '123456'])->assertRedirect('/');
        $this->assertAuthenticatedAs($this->usuario());
        $this->get('/')->assertSee('Administrador');
    }

    public function test_email_inexistente(): void
    {
        $this->post('/login', ['email' => 'nao@teste.com', 'password' => '123456'])->assertSessionHasErrors(['email' => 'E-mail não cadastrado']);
        $this->assertGuest();
    }

    public function test_senha_incorreta(): void
    {
        $this->post('/login', ['email' => 'admin@teste.com', 'password' => 'errada'])->assertSessionHasErrors(['password' => 'Senha incorreta']);
        $this->assertGuest();
    }

    public function test_campos_vazios(): void
    {
        $this->post('/login', [])->assertSessionHasErrors(['email' => 'Preencha e-mail e senha']);
    }

    public function test_rotas_protegidas(): void
    {
        foreach (['/', '/produtos', '/produtos/create', '/produtos/1/edit', '/estoque'] as $url) {
            $this->get($url)->assertRedirect('/login');
        }$this->post('/estoque', [])->assertRedirect('/login');
        $this->post('/produtos', [])->assertRedirect('/login');
        $this->put('/produtos/1', [])->assertRedirect('/login');
        $this->delete('/produtos/1')->assertRedirect('/login');
    }

    public function test_logout(): void
    {
        $this->actingAs($this->usuario())->post('/logout')->assertRedirect('/login');
        $this->assertGuest();
    }

    public function test_criar_editar_excluir_produto(): void
    {
        $this->actingAs($this->usuario())->post('/produtos', $this->dados())->assertRedirect('/produtos');
        $p = Produto::where('nome', 'Serrote')->firstOrFail();
        $this->put('/produtos/'.$p->id, array_merge($this->dados(), ['nome' => 'Serrote profissional']))->assertRedirect('/produtos');
        $this->assertDatabaseHas('produtos', ['id' => $p->id, 'nome' => 'Serrote profissional']);
        $this->delete('/produtos/'.$p->id)->assertRedirect('/produtos');
        $this->assertDatabaseMissing('produtos', ['id' => $p->id]);
    }

    public function test_validacoes_produto_e_old(): void
    {
        $this->actingAs($this->usuario())->from('/produtos/create')->post('/produtos', array_merge($this->dados(), ['nome' => '', 'marca' => str_repeat('x', 61), 'peso' => -1, 'estoque' => 1.5, 'estoque_minimo' => -2]))->assertSessionHasErrors(['nome', 'marca', 'peso', 'estoque', 'estoque_minimo'])->assertSessionHasInput('modelo', 'S1');
        $this->get('/produtos/create')->assertOk()->assertSee('O campo');
        $this->assertDatabaseCount('produtos', 4);
        $this->put('/produtos/1', [])->assertSessionHasErrors(['nome', 'peso', 'estoque']);
    }

    public function test_busca_em_todos_os_campos_e_sem_resultados(): void
    {
        $this->actingAs($this->usuario());
        foreach (['Borracha', 'Tramontina', 'MB-500', 'madeira'] as $termo) {
            $this->get('/produtos?busca='.urlencode($termo))->assertSee('Martelo de Borracha')->assertDontSee('Furadeira de Impacto');
        }
        $this->get('/produtos?busca=inexistente')->assertSee('Nenhum produto encontrado');
        $this->get('/produtos')->assertSee('Furadeira de Impacto');
    }

    public function test_exclusao_com_historico_bloqueada(): void
    {
        $this->actingAs($this->usuario())->delete('/produtos/1')->assertSessionHasErrors('produto');
        $this->assertDatabaseHas('produtos', ['id' => 1]);
        $this->assertDatabaseCount('movimentacoes', 3);
    }

    public function test_entrada_atualiza_estoque_e_responsavel(): void
    {
        $this->actingAs(Usuario::find(2))->post('/estoque', $this->movimento())->assertRedirect('/estoque')->assertSessionHas('success');
        $this->assertDatabaseHas('produtos', ['id' => 1, 'estoque' => 15]);
        $this->assertDatabaseHas('movimentacoes', ['produto_id' => 1, 'usuario_id' => 2, 'quantidade' => 3]);
    }

    public function test_saida_com_alerta(): void
    {
        $this->actingAs($this->usuario())->post('/estoque', $this->movimento(['tipo' => 'saida', 'quantidade' => 8]))->assertSessionHas('warning', 'Atenção: o estoque de Martelo de Borracha ficou em 4, abaixo do mínimo de 5');
        $this->assertDatabaseHas('produtos', ['id' => 1, 'estoque' => 4]);
        $this->assertDatabaseHas('movimentacoes', ['tipo' => 'saida', 'quantidade' => 8]);
    }

    public function test_saida_no_minimo_sem_alerta(): void
    {
        $this->actingAs($this->usuario())->post('/estoque', $this->movimento(['tipo' => 'saida', 'quantidade' => 7]))->assertSessionMissing('warning');
        $this->assertDatabaseHas('produtos', ['id' => 1, 'estoque' => 5]);
    }

    public function test_saida_maior_que_estoque_atomica(): void
    {
        $this->actingAs($this->usuario())->post('/estoque', $this->movimento(['tipo' => 'saida', 'quantidade' => 13]))->assertSessionHasErrors('quantidade');
        $this->assertDatabaseHas('produtos', ['id' => 1, 'estoque' => 12]);
        $this->assertDatabaseCount('movimentacoes', 3);
    }

    public function test_validacao_de_movimentacoes(): void
    {
        $this->actingAs($this->usuario());
        foreach ([['quantidade' => 0], ['quantidade' => 1.5], ['produto_id' => 999], ['tipo' => 'ajuste'], ['data_movimentacao' => now()->addDay()->toDateString()], ['data_movimentacao' => '2026-02-30']] as $invalidos) {
            $this->post('/estoque', $this->movimento($invalidos))->assertSessionHasErrors(array_keys($invalidos));
        }$this->assertDatabaseCount('movimentacoes', 3);
    }

    public function test_limite_de_estoque(): void
    {
        $this->actingAs($this->usuario())->post('/estoque', $this->movimento(['quantidade' => 2147483647]))->assertSessionHasErrors('quantidade');
        $this->assertDatabaseCount('movimentacoes', 3);
    }

    public function test_ordenacao_manual_acentos_e_caixa(): void
    {
        $nomes = ['zebra', 'Árvore', 'alicate', 'Época', 'Borracha'];
        $p = collect(array_map(fn ($n) => new Produto(['nome' => $n]), $nomes));
        $this->assertSame(['alicate', 'Árvore', 'Borracha', 'Época', 'zebra'], (new OrdenacaoService)->ordenar($p)->pluck('nome')->all());
        $this->assertCount(0, (new OrdenacaoService)->ordenar(collect()));
        $this->actingAs($this->usuario())->get('/estoque')->assertSeeInOrder(['Alicate Universal', 'Chave de Fenda Isolada', 'Furadeira de Impacto', 'Martelo de Borracha']);
    }

    public function test_telas_formularios_e_historico(): void
    {
        $this->actingAs($this->usuario());
        foreach (['/', '/produtos', '/produtos/create', '/produtos/1/edit', '/estoque'] as $url) {
            $this->get($url)->assertOk();
        }$this->get('/estoque')->assertSee('Histórico de movimentações')->assertSee('Ana Souza')->assertSee('Abaixo do mínimo');
    }

    public function test_historico_mais_recente_primeiro(): void
    {
        $this->actingAs($this->usuario())->post('/estoque', $this->movimento());
        $ids = $this->get('/estoque')->viewData('historico')->pluck('id')->all();
        $this->assertSame([4, 3, 2, 1], $ids);
    }

    public function test_schema_apenas_tres_tabelas_e_senhas_validas(): void
    {
        $nomes = array_column(DB::select("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"), 'name');
        $this->assertEqualsCanonicalizing(['usuario', 'produtos', 'movimentacoes'], $nomes);
        foreach (Usuario::all() as $u) {
            $this->assertTrue(Hash::check('123456',$u->password));
        }$this->assertDatabaseCount('usuario',3);
        $this->assertDatabaseCount('produtos',4);
        $this->assertDatabaseCount('movimentacoes',3);
    }
}
