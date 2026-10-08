<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class MovimentacaoRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return ['produto_id' => 'required|integer|exists:produtos,id', 'tipo' => 'required|in:entrada,saida', 'quantidade' => 'required|integer|min:1|max:2147483647', 'data_movimentacao' => 'required|date_format:Y-m-d|before_or_equal:today'];
    }

    public function messages(): array
    {
        return ['required' => 'O campo :attribute é obrigatório.', 'integer' => 'O campo :attribute deve ser inteiro.', 'exists' => 'Selecione um produto existente.', 'in' => 'Selecione entrada ou saída.', 'min' => 'A quantidade deve ser pelo menos 1.', 'max' => 'A quantidade excede o limite permitido.', 'date_format' => 'Informe uma data válida.', 'before_or_equal' => 'A data não pode ser futura.'];
    }

    public function attributes(): array
    {
        return ['produto_id' => 'produto', 'data_movimentacao' => 'data da movimentação'];
    }
}
