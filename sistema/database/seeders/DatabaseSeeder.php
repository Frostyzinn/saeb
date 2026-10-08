<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $dados = json_decode(file_get_contents(database_path('seeders/dados.json')), true, 512, JSON_THROW_ON_ERROR);
        DB::transaction(function () use ($dados) {
            foreach ($dados as $tabela => $registros) {
                DB::table($tabela)->insert($registros);
            }
        });
    }
}
