<?php

namespace App\Http\Controllers;

use App\Http\Requests\ProdutoRequest;
use App\Models\Produto;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;

class ProdutoController extends Controller
{
    public function index(Request $r)
    {
        $termo = $r->string('busca')->toString();

        return view('produtos.index', ['produtos' => Produto::buscar($termo)->get(), 'termo' => $termo]);
    }

    public function create()
    {
        return view('produtos.form', ['produto' => new Produto]);
    }

    public function edit(Produto $produto)
    {
        return view('produtos.form', compact('produto'));
    }

    public function store(ProdutoRequest $r)
    {
        Produto::create($r->validated());

        return redirect()->route('produtos.index')->with('success', 'Produto cadastrado com sucesso.');
    }

    public function update(ProdutoRequest $r, Produto $produto)
    {
        $produto->update($r->validated());

        return redirect()->route('produtos.index')->with('success', 'Produto atualizado com sucesso.');
    }

    public function destroy(Produto $produto)
    {
        DB::transaction(function () use ($produto) {
            $p = Produto::lockForUpdate()->findOrFail($produto->id);
            if ($p->movimentacoes()->exists()) {
                throw ValidationException::withMessages(['produto' => 'Não é possível excluir um produto com movimentações. O histórico deve ser preservado.']);
            }$p->delete();
        });

        return redirect()->route('produtos.index')->with('success', 'Produto excluído com sucesso.');
    }
}
