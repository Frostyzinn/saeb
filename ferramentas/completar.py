exec((__import__('pathlib').Path(__file__).parent/'gerar.py').read_text(encoding='utf-8').split("for p in (s/'database/migrations')")[0])
hash='$2y$10$5vL/0R8uFehTEJcUvA5u3.dZ4sxWe1lmAE6KNI2CTAMQtGGfzu5dK'
produtos=[dict(id=1,nome='Martelo de Borracha',marca='Tramontina',modelo='MB-500',material='Borracha e madeira',tamanho='30 cm',peso='0.50',tensao='Não se aplica',estoque=12,estoque_minimo=5),dict(id=2,nome='Chave de Fenda Isolada',marca='Vonder',modelo='CF-6',material='Aço e polímero',tamanho='20 cm',peso='0.15',tensao='Não se aplica',estoque=2,estoque_minimo=4),dict(id=3,nome='Alicate Universal',marca='Gedore',modelo='AU-8',material='Aço',tamanho='8 polegadas',peso='0.30',tensao='Não se aplica',estoque=8,estoque_minimo=3),dict(id=4,nome='Furadeira de Impacto',marca='Bosch',modelo='GSB-550',material='Aço e plástico',tamanho='25 cm',peso='1.80',tensao='220V',estoque=0,estoque_minimo=2)]
usuarios=[dict(idusuario=i,name=n,email=e,password=hash) for i,n,e in [(1,'Administrador','admin@teste.com'),(2,'Ana Souza','ana@teste.com'),(3,'Carlos Lima','carlos@teste.com')]]
movs=[dict(id=i,produto_id=i,usuario_id=i,tipo='entrada',quantidade=q,data_movimentacao='2026-01-15') for i,q in [(1,12),(2,2),(3,8)]]
data=dict(usuario=usuarios,produtos=produtos,movimentacoes=movs)
put('database/seeders/dados.json',json.dumps(data,ensure_ascii=False,indent=2))
put('database/seeders/DatabaseSeeder.php',r'''<?php
namespace Database\Seeders;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
class DatabaseSeeder extends Seeder {
 public function run(): void {
  $dados=json_decode(file_get_contents(database_path('seeders/dados.json')),true,512,JSON_THROW_ON_ERROR);
  DB::transaction(function()use($dados){foreach($dados as $tabela=>$registros){DB::table($tabela)->insert($registros);}});
 }
}''')
put('app/Services/ArquivoMigrationRepository.php',r'''<?php
namespace App\Services;
use Illuminate\Database\Migrations\MigrationRepositoryInterface;
use Illuminate\Support\Facades\DB;
// Mantém o controle de migrations fora do banco, que deve conter só três tabelas.
class ArquivoMigrationRepository implements MigrationRepositoryInterface {
 private $source;
 private array $memoria=[];
 private function path(): string {return storage_path('framework/migrations-'.md5((string)$this->source.config('database.connections.'.($this->source??config('database.default')).'.database')).'.json');}
 private function dados(): array {
  if(!DB::connection($this->source)->getSchemaBuilder()->hasTable('usuario')){return [];}
  if(app()->environment('testing')){return $this->memoria;}
  return is_file($this->path())?json_decode(file_get_contents($this->path()),true,512,JSON_THROW_ON_ERROR):[];
 }
 private function gravar(array $dados): void {if(app()->environment('testing')){$this->memoria=$dados;}else{file_put_contents($this->path(),json_encode($dados,JSON_THROW_ON_ERROR),LOCK_EX);}}
 public function getRan(){return array_keys($this->dados());}
 public function getMigrationBatches(){return $this->dados();}
 public function getMigrations($steps){return array_slice($this->registros(),0,$steps);}
 public function getMigrationsByBatch($batch){return array_values(array_filter($this->registros(),fn($r)=>$r->batch==$batch));}
 private function registros(): array {$r=[];foreach(array_reverse($this->dados(),true) as $m=>$b){$r[]=(object)['migration'=>$m,'batch'=>$b];}return $r;}
 public function getLast(){return $this->getMigrationsByBatch($this->getLastBatchNumber());}
 public function getLastBatchNumber(){return max([0,...array_values($this->dados())]);}
 public function getNextBatchNumber(){return $this->getLastBatchNumber()+1;}
 public function log($file,$batch){$dados=$this->dados();$dados[$file]=$batch;$this->gravar($dados);}
 public function delete($migration){$dados=$this->dados();unset($dados[$migration->migration]);$this->gravar($dados);}
 public function createRepository(){$this->gravar([]);}
 public function repositoryExists(){return DB::connection($this->source)->getSchemaBuilder()->hasTable('usuario');}
 public function deleteRepository(){if(!app()->environment('testing')&&is_file($this->path())){unlink($this->path());}$this->memoria=[];}
 public function setSource($name){$this->source=$name;}
}''')
put('app/Providers/AppServiceProvider.php',r'''<?php
namespace App\Providers;
use Illuminate\Support\ServiceProvider;
use App\Services\ArquivoMigrationRepository;
class AppServiceProvider extends ServiceProvider {
 public function register(): void {$this->app->singleton('migration.repository',fn()=>new ArquivoMigrationRepository);}
 public function boot(): void {\Illuminate\Pagination\Paginator::useBootstrapFive();}
}''')
sql='''-- Base de demonstração do SAEP. Importar em banco novo; não remove dados existentes.
CREATE DATABASE IF NOT EXISTS saep_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE saep_db;
CREATE TABLE usuario (idusuario INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL) ENGINE=InnoDB;
CREATE TABLE produtos (id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100) NOT NULL, marca VARCHAR(60) NOT NULL, modelo VARCHAR(60) NOT NULL, material VARCHAR(60) NOT NULL, tamanho VARCHAR(30) NOT NULL, peso DECIMAL(8,2) NOT NULL, tensao VARCHAR(30) NOT NULL, estoque INT NOT NULL DEFAULT 0, estoque_minimo INT NOT NULL DEFAULT 0) ENGINE=InnoDB;
CREATE TABLE movimentacoes (id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, produto_id INT UNSIGNED NOT NULL, usuario_id INT UNSIGNED NOT NULL, tipo ENUM('entrada','saida') NOT NULL, quantidade INT NOT NULL, data_movimentacao DATE NOT NULL, FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT ON UPDATE CASCADE, FOREIGN KEY (usuario_id) REFERENCES usuario(idusuario) ON DELETE RESTRICT ON UPDATE CASCADE) ENGINE=InnoDB;
'''
for table,rows in data.items():
 for row in rows:
  vals=[str(v) if isinstance(v,int) else "'"+v.replace("'","''")+"'" for v in row.values()]
  sql+=f"INSERT INTO {table} ({', '.join(row)}) VALUES ({', '.join(vals)});\n"
(root/'entregas/saep_db.sql').write_text(sql,encoding='utf-8')
put('tests/Feature/SistemaTest.php',r'''<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\{Usuario,Produto,Movimentacao};
use App\Services\OrdenacaoService;
use Illuminate\Support\Facades\{DB,Hash};
class SistemaTest extends TestCase {
 use RefreshDatabase;
 protected function setUp(): void {parent::setUp();$this->seed();}
 private function usuario(){return Usuario::first();}
 private function dados(): array {return ['nome'=>'Serrote','marca'=>'Vonder','modelo'=>'S1','material'=>'Aço','tamanho'=>'30 cm','peso'=>'0.60','tensao'=>'Não se aplica','estoque'=>10,'estoque_minimo'=>2];}
 private function movimento(array $dados=[]): array {return array_merge(['produto_id'=>1,'tipo'=>'entrada','quantidade'=>3,'data_movimentacao'=>now()->toDateString()],$dados);}
 public function test_login_com_sucesso(): void {$this->post('/login',['email'=>'admin@teste.com','password'=>'123456'])->assertRedirect('/');$this->assertAuthenticatedAs($this->usuario());$this->get('/')->assertSee('Administrador');}
 public function test_email_inexistente(): void {$this->post('/login',['email'=>'nao@teste.com','password'=>'123456'])->assertSessionHasErrors(['email'=>'E-mail não cadastrado']);$this->assertGuest();}
 public function test_senha_incorreta(): void {$this->post('/login',['email'=>'admin@teste.com','password'=>'errada'])->assertSessionHasErrors(['password'=>'Senha incorreta']);$this->assertGuest();}
 public function test_campos_vazios(): void {$this->post('/login',[])->assertSessionHasErrors(['email'=>'Preencha e-mail e senha']);}
 public function test_rotas_protegidas(): void {foreach(['/','/produtos','/produtos/create','/produtos/1/edit','/estoque'] as $url){$this->get($url)->assertRedirect('/login');}$this->post('/estoque',[])->assertRedirect('/login');$this->post('/produtos',[])->assertRedirect('/login');$this->put('/produtos/1',[])->assertRedirect('/login');$this->delete('/produtos/1')->assertRedirect('/login');}
 public function test_logout(): void {$this->actingAs($this->usuario())->post('/logout')->assertRedirect('/login');$this->assertGuest();}
 public function test_criar_editar_excluir_produto(): void {
  $this->actingAs($this->usuario())->post('/produtos',$this->dados())->assertRedirect('/produtos');$p=Produto::where('nome','Serrote')->firstOrFail();
  $this->put('/produtos/'.$p->id,array_merge($this->dados(),['nome'=>'Serrote profissional']))->assertRedirect('/produtos');$this->assertDatabaseHas('produtos',['id'=>$p->id,'nome'=>'Serrote profissional']);
  $this->delete('/produtos/'.$p->id)->assertRedirect('/produtos');$this->assertDatabaseMissing('produtos',['id'=>$p->id]);
 }
 public function test_validacoes_produto_e_old(): void {
  $this->actingAs($this->usuario())->from('/produtos/create')->post('/produtos',array_merge($this->dados(),['nome'=>'','marca'=>str_repeat('x',61),'peso'=>-1,'estoque'=>1.5,'estoque_minimo'=>-2]))->assertSessionHasErrors(['nome','marca','peso','estoque','estoque_minimo'])->assertSessionHasInput('modelo','S1');
  $this->get('/produtos/create')->assertOk()->assertSee('O campo');$this->assertDatabaseCount('produtos',4);
  $this->put('/produtos/1',[])->assertSessionHasErrors(['nome','peso','estoque']);
 }
 public function test_busca_em_todos_os_campos_e_sem_resultados(): void {
  $this->actingAs($this->usuario());foreach(['Borracha','Tramontina','MB-500','madeira'] as $termo){$this->get('/produtos?busca='.urlencode($termo))->assertSee('Martelo de Borracha')->assertDontSee('Furadeira de Impacto');}
  $this->get('/produtos?busca=inexistente')->assertSee('Nenhum produto encontrado');$this->get('/produtos')->assertSee('Furadeira de Impacto');
 }
 public function test_exclusao_com_historico_bloqueada(): void {$this->actingAs($this->usuario())->delete('/produtos/1')->assertSessionHasErrors('produto');$this->assertDatabaseHas('produtos',['id'=>1]);$this->assertDatabaseCount('movimentacoes',3);}
 public function test_entrada_atualiza_estoque_e_responsavel(): void {$this->actingAs(Usuario::find(2))->post('/estoque',$this->movimento())->assertRedirect('/estoque')->assertSessionHas('success');$this->assertDatabaseHas('produtos',['id'=>1,'estoque'=>15]);$this->assertDatabaseHas('movimentacoes',['produto_id'=>1,'usuario_id'=>2,'quantidade'=>3]);}
 public function test_saida_com_alerta(): void {$this->actingAs($this->usuario())->post('/estoque',$this->movimento(['tipo'=>'saida','quantidade'=>8]))->assertSessionHas('warning','Atenção: o estoque de Martelo de Borracha ficou em 4, abaixo do mínimo de 5');$this->assertDatabaseHas('produtos',['id'=>1,'estoque'=>4]);$this->assertDatabaseHas('movimentacoes',['tipo'=>'saida','quantidade'=>8]);}
 public function test_saida_no_minimo_sem_alerta(): void {$this->actingAs($this->usuario())->post('/estoque',$this->movimento(['tipo'=>'saida','quantidade'=>7]))->assertSessionHas('warning',null);$this->assertDatabaseHas('produtos',['id'=>1,'estoque'=>5]);}
 public function test_saida_maior_que_estoque_atomica(): void {$this->actingAs($this->usuario())->post('/estoque',$this->movimento(['tipo'=>'saida','quantidade'=>13]))->assertSessionHasErrors('quantidade');$this->assertDatabaseHas('produtos',['id'=>1,'estoque'=>12]);$this->assertDatabaseCount('movimentacoes',3);}
 public function test_validacao_de_movimentacoes(): void {$this->actingAs($this->usuario());foreach([['quantidade'=>0],['quantidade'=>1.5],['produto_id'=>999],['tipo'=>'ajuste'],['data_movimentacao'=>now()->addDay()->toDateString()],['data_movimentacao'=>'2026-02-30']] as $invalidos){$this->post('/estoque',$this->movimento($invalidos))->assertSessionHasErrors(array_keys($invalidos));}$this->assertDatabaseCount('movimentacoes',3);}
 public function test_limite_de_estoque(): void {$this->actingAs($this->usuario())->post('/estoque',$this->movimento(['quantidade'=>2147483647]))->assertSessionHasErrors('quantidade');$this->assertDatabaseCount('movimentacoes',3);}
 public function test_ordenacao_manual_acentos_e_caixa(): void {$nomes=['zebra','Árvore','alicate','Época','Borracha'];$p=collect(array_map(fn($n)=>new Produto(['nome'=>$n]),$nomes));$this->assertSame(['alicate','Árvore','Borracha','Época','zebra'],(new OrdenacaoService)->ordenar($p)->pluck('nome')->all());$this->assertCount(0,(new OrdenacaoService)->ordenar(collect()));$this->actingAs($this->usuario())->get('/estoque')->assertSeeInOrder(['Alicate Universal','Chave de Fenda Isolada','Furadeira de Impacto','Martelo de Borracha']);}
 public function test_telas_formularios_e_historico(): void {$this->actingAs($this->usuario());foreach(['/','/produtos','/produtos/create','/produtos/1/edit','/estoque'] as $url){$this->get($url)->assertOk();}$this->get('/estoque')->assertSee('Histórico de movimentações')->assertSee('Ana Souza')->assertSee('Abaixo do mínimo');}
 public function test_historico_mais_recente_primeiro(): void {$this->actingAs($this->usuario())->post('/estoque',$this->movimento());$ids=$this->get('/estoque')->viewData('historico')->pluck('id')->all();$this->assertSame([4,3,2,1],$ids);}
 public function test_schema_apenas_tres_tabelas_e_senhas_validas(): void {$nomes=array_column(DB::select("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"),'name');$this->assertEqualsCanonicalizing(['usuario','produtos','movimentacoes'],$nomes);foreach(Usuario::all() as $u){$this->assertTrue(Hash::check('123456',$u->password));}$this->assertDatabaseCount('usuario',3);$this->assertDatabaseCount('produtos',4);$this->assertDatabaseCount('movimentacoes',3);}
}''')
print('Seed, SQL, repositório e testes gerados.')
