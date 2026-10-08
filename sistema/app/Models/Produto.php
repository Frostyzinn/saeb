<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Produto extends Model
{
    protected $table = 'produtos';

    public $timestamps = false;

    protected $fillable = ['nome', 'marca', 'modelo', 'material', 'tamanho', 'peso', 'tensao', 'estoque', 'estoque_minimo'];

    protected function casts(): array
    {
        return ['peso' => 'decimal:2', 'estoque' => 'integer', 'estoque_minimo' => 'integer'];
    }

    public function movimentacoes()
    {
        return $this->hasMany(Movimentacao::class);
    }

    public function abaixoDoMinimo(): bool
    {
        return $this->estoque < $this->estoque_minimo;
    }

    public function scopeBuscar($query, $termo)
    {
        return $query->when($termo !== null && $termo !== '', fn ($q) => $q->where(function ($q) use ($termo) {
            foreach (['nome', 'marca', 'modelo', 'material'] as $campo) {
                $q->orWhere($campo, 'like', '%'.$termo.'%');
            }
        }));
    }
}
