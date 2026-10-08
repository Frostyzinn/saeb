<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Movimentacao extends Model
{
    protected $table = 'movimentacoes';

    public $timestamps = false;

    protected $fillable = ['produto_id', 'usuario_id', 'tipo', 'quantidade', 'data_movimentacao'];

    protected function casts(): array
    {
        return ['data_movimentacao' => 'date', 'quantidade' => 'integer'];
    }

    public function produto()
    {
        return $this->belongsTo(Produto::class);
    }

    public function usuario()
    {
        return $this->belongsTo(Usuario::class, 'usuario_id', 'idusuario');
    }
}
