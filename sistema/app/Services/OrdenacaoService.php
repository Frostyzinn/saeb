<?php

namespace App\Services;

use Illuminate\Support\Collection;
use Illuminate\Support\Str;

class OrdenacaoService
{
    public function ordenar(Collection $produtos): Collection
    {
        $itens = $produtos->all();
        // Insertion Sort: desloca os maiores à direita e insere o elemento na posição correta.
        for ($i = 1; $i < count($itens); $i++) {
            $atual = $itens[$i];
            $chave = $this->normalizar($atual->nome);
            $j = $i - 1;
            while ($j >= 0 && strcmp($this->normalizar($itens[$j]->nome), $chave) > 0) {
                $itens[$j + 1] = $itens[$j];
                $j--;
            }
            $itens[$j + 1] = $atual;
        }

        return collect($itens);
    }

    private function normalizar(string $nome): string
    {
        return Str::ascii(mb_strtolower($nome, 'UTF-8'));
    }
}
