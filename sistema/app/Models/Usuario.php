<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;

class Usuario extends Authenticatable
{
    protected $table = 'usuario';

    protected $primaryKey = 'idusuario';

    public $timestamps = false;

    protected $fillable = ['name', 'email', 'password'];

    protected $hidden = ['password'];

    protected function casts(): array
    {
        return ['password' => 'hashed'];
    }

    public function getRememberTokenName()
    {
        return '';
    }

    public function movimentacoes()
    {
        return $this->hasMany(Movimentacao::class, 'usuario_id', 'idusuario');
    }
}
