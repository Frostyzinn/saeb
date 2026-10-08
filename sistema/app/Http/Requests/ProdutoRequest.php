<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ProdutoRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        $r = [];
        foreach (['nome' => 100, 'marca' => 60, 'modelo' => 60, 'material' => 60, 'tamanho' => 30, 'tensao' => 30] as $c => $n) {
            $r[$c] = ['required', 'string', 'max:'.$n];
        }

        return $r + ['peso' => ['required', 'numeric', 'min:0', 'max:999999.99'], 'estoque' => ['required', 'integer', 'min:0', 'max:2147483647'], 'estoque_minimo' => ['required', 'integer', 'min:0', 'max:2147483647']];
    }

    public function messages(): array
    {
        return ['required' => 'O campo :attribute é obrigatório.', 'string' => 'O campo :attribute deve ser um texto.', 'max' => 'O campo :attribute excede o limite permitido (:max).', 'numeric' => 'O campo :attribute deve ser numérico.', 'integer' => 'O campo :attribute deve ser inteiro.', 'min' => 'O campo :attribute deve ser pelo menos :min.'];
    }

    public function attributes(): array
    {
        return ['tensao' => 'tensão', 'estoque_minimo' => 'estoque mínimo'];
    }
}
