<?php

namespace App\Http\Controllers;

use App\Models\Movimentacao;
use App\Models\Produto;

class HomeController extends Controller
{
    public function index()
    {
        return view('home', ['total' => Produto::count(), 'alertas' => Produto::whereColumn('estoque', '<', 'estoque_minimo')->count(), 'movimentos' => Movimentacao::count()]);
    }
}
