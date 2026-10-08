# Entrega 08 - Casos de teste

## 8.1 Casos positivos e negativos por requisito

Base: três usuários, quatro produtos e três entradas de 15/01/2026. Reiniciar a base de teste para cada caso; nunca reiniciar uma base real. Pré-condição padrão: sessão admin ativa e base inicial, exceto casos de login/visitante, que usam sessão encerrada. Casos vazios/nomes especiais usam base isolada. Os passos abaixo incluem os dados de entrada.

| ID | Requisito | Pré-condição | Passos e dados de entrada | Resultado esperado |
|---|---|---|---|---|
| CT01P | RF01 (4.1) | Sem sessão | Enviar admin@teste.com / 123456 no login. | Painel aberto com sessão autenticada. |
| CT01N | RF01 (4.1) | Sem sessão | Enviar admin@teste.com / errada. | Senha incorreta; permanece no login sem sessão autenticada. |
| CT02P | RF02 (4.2) | Sem sessão | Abrir login em 1280 e 390 px de largura. | Campos legíveis, botão acessível e texto em português. |
| CT02N | RF02 (4.2) | Sem sessão | Abrir login e enviar dados inválidos em 390 px. | Mensagem visível sem sobreposição dos campos. |
| CT03P | RF03 (5.1.1) | Base isolada; admin autenticado salvo indicação nos passos | Entrar como Ana (ana@teste.com / 123456). | Ana Souza exibida no painel e cabeçalho. |
| CT03N | RF03 (5.1.1) | Base isolada; admin autenticado salvo indicação nos passos | Abrir painel sem sessão. | Redirecionamento ao login; nenhum nome de usuário exposto. |
| CT04P | RF04 (5.1.2) | Base isolada; admin autenticado salvo indicação nos passos | Com sessão ativa, clicar Sair. | Sessão invalidada, token regenerado e login aberto. |
| CT04N | RF04 (5.1.2) | Base isolada; admin autenticado salvo indicação nos passos | Enviar POST /logout sem token em navegador. | HTTP 419; sessão não encerrada pelo pedido inválido. |
| CT05P | RF05 (5.1.3) | Base isolada; admin autenticado salvo indicação nos passos | Clicar Cadastro de Produto. | Tabela de produtos aberta. |
| CT05N | RF05 (5.1.3) | Base isolada; admin autenticado salvo indicação nos passos | Abrir /produtos sem login. | Redirecionamento ao login. |
| CT06P | RF06 (5.1.4) | Base isolada; admin autenticado salvo indicação nos passos | Clicar Gestão de Estoque. | Formulário e listagem de estoque abertos. |
| CT06N | RF06 (5.1.4) | Base isolada; admin autenticado salvo indicação nos passos | Abrir /estoque sem login. | Redirecionamento ao login. |
| CT07P | RF07 (5.1.5) | Base isolada; admin autenticado salvo indicação nos passos | Abrir painel autenticado em 390 px. | Indicadores e acessos empilhados e legíveis. |
| CT07N | RF07 (5.1.5) | Base isolada; admin autenticado salvo indicação nos passos | Abrir painel após logout. | Login exibido, sem indicadores acessíveis. |
| CT08P | RF08 (6.1.1) | Base isolada; admin autenticado salvo indicação nos passos | Abrir /produtos com base semeada. | Quatro produtos apresentados com suas características. |
| CT08N | RF08 (6.1.1) | Base isolada; admin autenticado salvo indicação nos passos | Abrir tabela em base de teste sem produtos. | Nenhum produto encontrado. |
| CT09P | RF09 (6.1.2) | Base isolada; admin autenticado salvo indicação nos passos | Buscar MB-500 e depois clicar Limpar busca. | Martelo encontrado; limpeza restaura quatro produtos. |
| CT09N | RF09 (6.1.2) | Base isolada; admin autenticado salvo indicação nos passos | Buscar inexistente. | Nenhum produto encontrado; termo permanece no campo. |
| CT10P | RF10 (6.1.3) | Base isolada; admin autenticado salvo indicação nos passos | Novo produto; preencher Serrote/Vonder/S1/Aço/30 cm/0.60/Não se aplica/10/2; Salvar. | Produto persistido e mensagem de sucesso. |
| CT10N | RF10 (6.1.3) | Base isolada; admin autenticado salvo indicação nos passos | Salvar com nome vazio. | Cadastro rejeitado com erro; nenhum produto criado. |
| CT11P | RF11 (6.1.4) | Base isolada; admin autenticado salvo indicação nos passos | Editar Martelo e mudar marca para Vonder; Salvar. | Produto atualizado e mensagem de sucesso. |
| CT11N | RF11 (6.1.4) | Base isolada; admin autenticado salvo indicação nos passos | Editar com peso -1. | Alteração rejeitada e dados originais preservados. |
| CT12P | RF12 (6.1.5) | Base isolada; admin autenticado salvo indicação nos passos | Criar Serrote sem movimentos; Excluir; confirmar. | Produto excluído com mensagem de sucesso. |
| CT12N | RF12 (6.1.5) | Base isolada; admin autenticado salvo indicação nos passos | Excluir Martelo com histórico. | Mensagem clara de bloqueio; produto e histórico preservados. |
| CT13P | RF13 (6.1.6) | Base isolada; admin autenticado salvo indicação nos passos | Salvar produto com valores válidos e peso zero. | Produto salvo; zero permitido. |
| CT13N | RF13 (6.1.6) | Base isolada; admin autenticado salvo indicação nos passos | Enviar marca com 61 caracteres, peso -1, estoque 1.5 e mínimo -2. | Erros visíveis por campo e no topo; entradas válidas preservadas. |
| CT14P | RF14 (6.1.7) | Base isolada; admin autenticado salvo indicação nos passos | Clicar Voltar à interface principal. | Painel autenticado aberto. |
| CT14N | RF14 (6.1.7) | Base isolada; admin autenticado salvo indicação nos passos | Após expiração da sessão, acessar o destino do botão. | Login solicitado. |
| CT15P | RF15 (6.1.8) | Base isolada; admin autenticado salvo indicação nos passos | Abrir tabela e formulário em 390 px. | Formulário adaptado e tabela com rolagem horizontal. |
| CT15N | RF15 (6.1.8) | Base isolada; admin autenticado salvo indicação nos passos | Enviar dados inválidos em tela estreita. | Erros legíveis e ações continuam acessíveis. |
| CT16P | RF16 (7.1.1) | Base isolada; admin autenticado salvo indicação nos passos | Criar nomes zebra, Árvore, alicate, Época e Borracha em base de teste e abrir estoque. | alicate, Árvore, Borracha, Época, zebra nessa ordem. |
| CT16N | RF16 (7.1.1) | Base isolada; admin autenticado salvo indicação nos passos | Executar ordenação sobre coleção vazia. | Coleção vazia retornada sem erro. |
| CT17P | RF17 (7.1.2) | Base isolada; admin autenticado salvo indicação nos passos | Selecionar Martelo e Entrada. | Escolhas submetidas e movimento registrado. |
| CT17N | RF17 (7.1.2) | Base isolada; admin autenticado salvo indicação nos passos | Enviar tipo ajuste ou produto 999 inexistente. | Pedido rejeitado sem alteração de estoque ou histórico. |
| CT18P | RF18 (7.1.3) | Base isolada; admin autenticado salvo indicação nos passos | Registrar com data de hoje. | Data armazenada e exibida no histórico. |
| CT18N | RF18 (7.1.3) | Base isolada; admin autenticado salvo indicação nos passos | Enviar amanhã ou 2026-02-30. | Data rejeitada sem registrar movimento. |
| CT19P | RF19 (7.1.4) | Base isolada; admin autenticado salvo indicação nos passos | Sair 8 unidades do Martelo (12 em estoque, mínimo 5). | Estoque 4, movimento salvo e alerta destacado com nome, saldo e mínimo. |
| CT19N | RF19 (7.1.4) | Base isolada; admin autenticado salvo indicação nos passos | Sair 7 unidades do Martelo (saldo 5). | Operação confirmada sem falso alerta de estoque mínimo. |
| CT20P | RF20 (7.1.5) | Base isolada; admin autenticado salvo indicação nos passos | Abrir estoque em 390 px. | Formulário, produtos e histórico legíveis. |
| CT20N | RF20 (7.1.5) | Base isolada; admin autenticado salvo indicação nos passos | Abrir tela sem produtos em base de teste. | Estado vazio legível, sem erro na página. |
| CT21P | RF21 (7 adicional) | Base isolada; admin autenticado salvo indicação nos passos | Sair exatamente 12 do Martelo. | Saldo zero e saída registrada com alerta. |
| CT21N | RF21 (7 adicional) | Base isolada; admin autenticado salvo indicação nos passos | Sair 13 do Martelo ou informar quantidade 0/1.5. | Erro claro; saldo e histórico não alterados. |
| CT22P | RF22 (7 adicional) | Base isolada; admin autenticado salvo indicação nos passos | Ana registra entrada 3 no Martelo. | Saldo 15 e movimento de Ana, dentro da mesma transação. |
| CT22N | RF22 (7 adicional) | Base isolada; admin autenticado salvo indicação nos passos | Entrar 2147483647 unidades no Martelo. | Limite rejeitado e transação sem alterações. |
| CT23P | RF23 (7 adicional) | Base isolada; admin autenticado salvo indicação nos passos | Registrar entrada hoje e consultar histórico. | Nova entrada antes das antigas; todos os campos exibidos. |
| CT23N | RF23 (7 adicional) | Base isolada; admin autenticado salvo indicação nos passos | Abrir histórico em base de teste sem movimentações. | Nenhuma movimentação registrada; sem dados inventados. |
| CT24P | RF24 (7 adicional) | Base isolada; admin autenticado salvo indicação nos passos | Clicar Voltar à interface principal no estoque. | Painel aberto. |
| CT24N | RF24 (7 adicional) | Base isolada; admin autenticado salvo indicação nos passos | Acessar retorno com sessão encerrada. | Login solicitado. |
| CT25P | RF25 (Segurança) | Base isolada; admin autenticado salvo indicação nos passos | Entrar com credenciais válidas e consultar formulário com token. | Login aceito e formulário contém token; senha no banco é bcrypt. |
| CT25N | RF25 (Segurança) | Base isolada; admin autenticado salvo indicação nos passos | Enviar POST /estoque sem token em sessão real. | HTTP 419 e estoque inalterado. |

## 8.2 Ferramentas e ambiente

- PHP 8.2.18, Laravel 11.57.0, PHPUnit 11.5.57.
- Testes Feature: `cd sistema` e `php artisan test`; SQLite em memória, explicitamente forçado em phpunit.xml. Não acessam saep_db.
- Integração local: MySQL 8.3.0, Windows 11 build 22631, WampServer, servidor Artisan na porta 8000.
- Navegador: Codex In-app Browser. Bootstrap 5.3.3 armazenado localmente.
- Casos de layout e CSRF devem ser verificados por navegador; o middleware CSRF é desabilitado pelo Laravel nos testes Feature.
- Resultados efetivamente executados estão em `verificacao.md`; a tabela acima descreve expectativas, não presume que todos os casos manuais foram executados.
