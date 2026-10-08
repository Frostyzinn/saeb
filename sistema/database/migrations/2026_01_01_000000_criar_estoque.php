<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('usuario', function (Blueprint $t) {
            $t->engine = 'InnoDB';
            $t->increments('idusuario');
            $t->string('name', 100);
            $t->string('email', 100)->unique();
            $t->string('password', 255);
        });
        Schema::create('produtos', function (Blueprint $t) {
            $t->engine = 'InnoDB';
            $t->increments('id');
            $t->string('nome', 100);
            $t->string('marca', 60);
            $t->string('modelo', 60);
            $t->string('material', 60);
            $t->string('tamanho', 30);
            $t->decimal('peso', 8, 2);
            $t->string('tensao', 30);
            $t->integer('estoque')->default(0);
            $t->integer('estoque_minimo')->default(0);
        });
        Schema::create('movimentacoes', function (Blueprint $t) {
            $t->engine = 'InnoDB';
            $t->increments('id');
            $t->unsignedInteger('produto_id');
            $t->unsignedInteger('usuario_id');
            $t->enum('tipo', ['entrada', 'saida']);
            $t->integer('quantidade');
            $t->date('data_movimentacao');
            $t->foreign('produto_id')->references('id')->on('produtos')->restrictOnDelete()->cascadeOnUpdate();
            $t->foreign('usuario_id')->references('idusuario')->on('usuario')->restrictOnDelete()->cascadeOnUpdate();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('movimentacoes');
        Schema::dropIfExists('produtos');
        Schema::dropIfExists('usuario');
    }
};
