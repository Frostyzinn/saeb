<?php

namespace App\Http\Controllers;

use App\Http\Requests\MovimentacaoRequest;
use App\Models\Movimentacao;
use App\Models\Produto;
use App\Services\OrdenacaoService;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;

class EstoqueController extends Controller
{
    public function index(OrdenacaoService $ordenacao)
    {
        return view('estoque.index', ['produtos' => $ordenacao->ordenar(Produto::all()), 'historico' => Movimentacao::with(['produto', 'usuario'])->orderByDesc('data_movimentacao')->orderByDesc('id')->paginate(20)]);
    }

    public function registrar(MovimentacaoRequest $r)
    {
        $alerta = DB::transaction(function () use ($r) {
            $p = Produto::lockForUpdate()->findOrFail($r->validated('produto_id'));
            $q = (int) $r->validated('quantidade');
            $tipo = $r->validated('tipo');
            if ($tipo === 'saida' && $q > $p->estoque) {
                throw ValidationException::withMessages(['quantidade' => 'Saída maior que o estoque disponível ('.$p->estoque.').']);
            }
            $novo = $p->estoque + ($tipo === 'entrada' ? $q : -$q);
            if ($novo > 2147483647) {
                throw ValidationException::withMessages(['quantidade' => 'A entrada ultrapassa o limite de estoque.']);
            }
            Movimentacao::create($r->validated() + ['usuario_id' => $r->user()->idusuario]);
            $p->update(['estoque' => $novo]);

            return $tipo === 'saida' && $p->abaixoDoMinimo() ? "Atenção: o estoque de {$p->nome} ficou em {$p->estoque}, abaixo do mínimo de {$p->estoque_minimo}" : null;
        });

        return redirect()->route('estoque.index')->with('success', 'Movimentação registrada com sucesso.')->with('warning', $alerta);
    }
}
