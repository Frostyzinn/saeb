<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\EstoqueController;
use App\Http\Controllers\HomeController;
use App\Http\Controllers\ProdutoController;
use Illuminate\Support\Facades\Route;

Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'login'])->name('login');
    Route::post('/login', [AuthController::class, 'autenticar'])->middleware('throttle:10,1')->name('login.autenticar');
});
Route::middleware('auth')->group(function () {
    Route::get('/', [HomeController::class, 'index'])->name('home');
    Route::post('/logout', [AuthController::class, 'logout'])->name('logout');
    Route::resource('produtos', ProdutoController::class)->except('show');
    Route::get('/estoque', [EstoqueController::class, 'index'])->name('estoque.index');
    Route::post('/estoque', [EstoqueController::class, 'registrar'])->name('estoque.registrar');
});
