# Verificação da entrega

Resultados executados no ambiente local:

- `php artisan test`: 20 testes Feature aprovados, 120 assertions, SQLite em memória.
- SQL importado pelo cliente MySQL 8.3.0, sem erro, em saep_db novo: usuario 3, produtos 4, movimentacoes 3.
- `php artisan migrate:fresh --seed`, `migrate:rollback` e `migrate --seed` executados sem erro no banco de demonstração criado nesta tarefa.
- `migrate:status` registra a migration; novo `migrate` não repete a criação.
- MySQL consultado: exatamente três tabelas, todas InnoDB, duas FKs com DELETE RESTRICT e UPDATE CASCADE.
- Dados das três tabelas comparados com o JSON que origina SQL e seeder: iguais, inclusive hashes bcrypt.
- Rollback de uma transação MySQL que altera saldo e cria histórico: ambos revertidos. Exclusão direta de produto com movimento: rejeitada pelo MySQL, código 1451.
- Navegador: login → painel → catálogo → painel → estoque → saída 8 do Martelo → alerta de saldo 4 abaixo do mínimo 5 → histórico com responsável e data → logout. Captura estoque_verificado.jpg registra esse teste.
- Banco de demonstração restaurado ao seeder após o teste de saída. painel_verificado.jpg mostra os dados iniciais restaurados.
- Layout de login e catálogo conferido em largura 390 px; tabela tem rolagem horizontal. Painel e estoque conferidos no navegador padrão. DER PNG inspecionado visualmente.
- Pint aplicado ao PHP. Templates Blade compilados e rotas listadas sem erro.

O aviso local de Xdebug sobre acesso ao arquivo de log não impede os comandos. A frase padrão “Creating migration table” do Artisan se refere à preparação do repositório; neste projeto o repositório é JSON e nenhuma quarta tabela é criada.

A tabela de casos documenta testes positivos e negativos para os 25 requisitos. Os 20 testes automatizados cobrem os cenários centrais; não se afirma que cada caso manual da tabela foi executado individualmente.
