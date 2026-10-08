# SAEP - Almoxarifado

Sistema do simulado SENAI, em português, com login manual, catálogo de ferramentas, entradas/saídas, alertas e histórico.

## Executar

O projeto nesta máquina já tem dependências, chave e banco inicializados. No PowerShell:

```powershell
cd C:\wamp64\www\Saep\sistema
php artisan serve
```

Abra http://127.0.0.1:8000. Usuários: `admin@teste.com`, `ana@teste.com`, `carlos@teste.com`; senha de todos: `123456`.

## Instalar a partir do ZIP

Requer PHP 8.2.18 e MySQL. Dentro de `sistema`:

```powershell
composer install
Copy-Item .env.example .env
php artisan key:generate
```

Crie `saep_db` no MySQL (utf8mb4) e ajuste DB_USERNAME/DB_PASSWORD no .env. Escolha somente uma forma de popular a base:

1. `php artisan migrate:fresh --seed` em um banco novo ou descartável. Este comando APAGA todas as tabelas do banco configurado.
2. Importe `entregas/saep_db.sql` (ou o SQL na raiz do ZIP) em saep_db vazio, pelo Workbench ou cliente MySQL. Não execute o seeder depois da importação, pois os dados já estão incluídos.

Depois: `php artisan serve`. `php artisan test` usa SQLite em memória e não altera MySQL.

## Decisões

- A pasta selecionada era vazia. Nome completo não foi fornecido: ZIP chamado `Aluno_SAEP.zip`, com pasta `Aluno_SAEP`; renomeie ambos com seu nome completo antes da entrega.
- As três tabelas não têm timestamps nem remember_token. Sem opção Lembrar-me. Sessões/cache usam arquivo e filas usam sync.
- PKs e FKs são INT UNSIGNED compatíveis, com auto incremento nas PKs. Evitamos `$table->id()` porque gera BIGINT, divergente do INT pedido.
- Para manter literalmente só três tabelas, `ArquivoMigrationRepository` substitui o repositório de migrations do Laravel por JSON em storage/framework. Em testes usa memória. Preserve esse arquivo junto da instalação para controlar rollback/status; `migrate:fresh` reconhece a remoção das tabelas. Após importar SQL, use o sistema diretamente, sem executar migrate sobre essas tabelas já criadas. O ZIP não inclui o journal da máquina de desenvolvimento.
- Produtos com movimentações não podem ser excluídos: preserva rastreabilidade e respeita RESTRICT. A exclusão exige confirmação no navegador.
- Estoque inicial/editável no cadastro atende ao enunciado literalmente. Alteração direta no cadastro não gera movimentação; para rastrear entradas e saídas, use Gestão de Estoque. Não há edição/exclusão de movimentos.
- Seed e SQL usam o mesmo conjunto (`database/seeders/dados.json`), com três usuários, quatro produtos e três movimentos. O saldo corresponde às entradas iniciais. Chave e furadeira começam abaixo do mínimo.
- As migrations fixam InnoDB explicitamente, pois o padrão do Wamp desta máquina era MyISAM; assim as FKs, transações e travas funcionam. Quantidades são inteiras; saldo é protegido contra overflow INT. Peso limitado a DECIMAL(8,2). Datas futuras são avaliadas no fuso America/Sao_Paulo. Histórico ordenado por data decrescente e id decrescente, paginado em 20.
- Bootstrap 5.3.3 está em public/css; funciona sem CDN. `public` é a raiz web: nunca exponha a pasta do projeto ou .env no Apache.
- Laravel 11 é a versão exigida, embora o Composer tenha informado advisories para ela neste ambiente. A instalação inicial usou `--no-security-blocking` para cumprir o simulado local. Antes de uso real, atualizar framework/dependências e trocar credenciais de demonstração. O ZIP conserva composer.lock para instalação reproduzível.

## Ordenação

`app/Services/OrdenacaoService.php` implementa Insertion Sort estável sobre `Produto::all()`. Normaliza com mb_strtolower e transliteração Str::ascii; compara chaves e desloca elementos manualmente. Não usa orderBy, sort, usort ou sortBy na listagem de produtos do estoque. Custo médio/pior O(n²), melhor O(n), memória auxiliar O(1) para ordenar o array, além da coleção/array recebido. Foi escolhido por ser simples de explicar e adequado ao pequeno catálogo do simulado. A normalização também depende do comprimento dos nomes, limitado a 100 caracteres.

## Arquivos de entrega

`entregas/` contém requisitos, DER em Mermaid e PNG, SQL, casos de teste e infraestrutura. `Aluno_SAEP.zip` reúne esses documentos e `sistema/` sem vendor, node_modules, .env, caches ou logs. O README também está dentro do sistema e na raiz do ZIP.

## Checklist do caderno

- [x] 4.1 — Autenticar por e-mail e senha, distinguindo campos vazios, e-mail inexistente e senha incorreta. Implementação: `AuthController e auth/login`.
- [x] 4.2 — Exibir login limpo, responsivo e em português. Implementação: `auth/login e layouts/app`.
- [x] 5.1.1 — Exibir o nome do usuário autenticado. Implementação: `home e layouts/app`.
- [x] 5.1.2 — Encerrar sessão via POST com CSRF e retornar ao login. Implementação: `AuthController::logout e layouts/app`.
- [x] 5.1.3 — Acessar Cadastro de Produto pelo painel. Implementação: `home → produtos.index`.
- [x] 5.1.4 — Acessar Gestão de Estoque pelo painel. Implementação: `home → estoque.index`.
- [x] 5.1.5 — Exibir painel limpo e responsivo. Implementação: `home e app.css`.
- [x] 6.1.1 — Carregar automaticamente todos os produtos em tabela. Implementação: `ProdutoController::index e produtos/index`.
- [x] 6.1.2 — Buscar por nome, marca, modelo ou material, manter termo e permitir limpar busca. Implementação: `Produto::scopeBuscar e produtos/index`.
- [x] 6.1.3 — Cadastrar novo produto. Implementação: `ProdutoController::store e produtos/form`.
- [x] 6.1.4 — Editar produto existente. Implementação: `ProdutoController::update e produtos/form`.
- [x] 6.1.5 — Excluir com confirmação e impedir exclusão com movimentações. Implementação: `ProdutoController::destroy e confirmação em produtos/index`.
- [x] 6.1.6 — Validar campos obrigatórios, limites textuais, peso não negativo e estoques inteiros não negativos; preservar dados e mostrar erros no topo e nos campos. Implementação: `ProdutoRequest, produtos/form e x-alertas`.
- [x] 6.1.7 — Retornar à interface principal a partir do cadastro. Implementação: `produtos/index e produtos/form`.
- [x] 6.1.8 — Exibir cadastro responsivo em português. Implementação: `produtos/*, Bootstrap e app.css`.
- [x] 7.1.1 — Listar estoque em ordem alfabética com algoritmo manual, ignorando caixa e acentos. Implementação: `OrdenacaoService e EstoqueController::index`.
- [x] 7.1.2 — Selecionar produto e escolher entrada ou saída por radio buttons. Implementação: `estoque/index e MovimentacaoRequest`.
- [x] 7.1.3 — Exigir data válida e não futura na movimentação. Implementação: `MovimentacaoRequest e estoque/index`.
- [x] 7.1.4 — Alertar após saída abaixo do mínimo e destacar produtos críticos com badge vermelha. Implementação: `EstoqueController::registrar, x-alertas e badge`.
- [x] 7.1.5 — Exibir gestão de estoque limpa e responsiva. Implementação: `estoque/index, Bootstrap e app.css`.

Consulte `entregas/verificacao.md` para resultados de execução, importação e testes.
