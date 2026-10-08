from pathlib import Path
import json,zipfile
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];e=root/'entregas';s=root/'sistema'
def doc(nome,t): (e/nome).write_text(t.strip()+'\n',encoding='utf-8')
requisitos=[
('4.1','Autenticar por e-mail e senha, distinguindo campos vazios, e-mail inexistente e senha incorreta.','Enviar admin@teste.com / 123456 no login.','Painel aberto com sessão autenticada.','Enviar admin@teste.com / errada.','Senha incorreta; permanece no login sem sessão autenticada.'),
('4.2','Exibir login limpo, responsivo e em português.','Abrir login em 1280 e 390 px de largura.','Campos legíveis, botão acessível e texto em português.','Abrir login e enviar dados inválidos em 390 px.','Mensagem visível sem sobreposição dos campos.'),
('5.1.1','Exibir o nome do usuário autenticado.','Entrar como Ana (ana@teste.com / 123456).','Ana Souza exibida no painel e cabeçalho.','Abrir painel sem sessão.','Redirecionamento ao login; nenhum nome de usuário exposto.'),
('5.1.2','Encerrar sessão via POST com CSRF e retornar ao login.','Com sessão ativa, clicar Sair.','Sessão invalidada, token regenerado e login aberto.','Enviar POST /logout sem token em navegador.','HTTP 419; sessão não encerrada pelo pedido inválido.'),
('5.1.3','Acessar Cadastro de Produto pelo painel.','Clicar Cadastro de Produto.','Tabela de produtos aberta.','Abrir /produtos sem login.','Redirecionamento ao login.'),
('5.1.4','Acessar Gestão de Estoque pelo painel.','Clicar Gestão de Estoque.','Formulário e listagem de estoque abertos.','Abrir /estoque sem login.','Redirecionamento ao login.'),
('5.1.5','Exibir painel limpo e responsivo.','Abrir painel autenticado em 390 px.','Indicadores e acessos empilhados e legíveis.','Abrir painel após logout.','Login exibido, sem indicadores acessíveis.'),
('6.1.1','Carregar automaticamente todos os produtos em tabela.','Abrir /produtos com base semeada.','Quatro produtos apresentados com suas características.','Abrir tabela em base de teste sem produtos.','Nenhum produto encontrado.'),
('6.1.2','Buscar por nome, marca, modelo ou material, manter termo e permitir limpar busca.','Buscar MB-500 e depois clicar Limpar busca.','Martelo encontrado; limpeza restaura quatro produtos.','Buscar inexistente.','Nenhum produto encontrado; termo permanece no campo.'),
('6.1.3','Cadastrar novo produto.','Novo produto; preencher Serrote/Vonder/S1/Aço/30 cm/0.60/Não se aplica/10/2; Salvar.','Produto persistido e mensagem de sucesso.','Salvar com nome vazio.','Cadastro rejeitado com erro; nenhum produto criado.'),
('6.1.4','Editar produto existente.','Editar Martelo e mudar marca para Vonder; Salvar.','Produto atualizado e mensagem de sucesso.','Editar com peso -1.','Alteração rejeitada e dados originais preservados.'),
('6.1.5','Excluir com confirmação e impedir exclusão com movimentações.','Criar Serrote sem movimentos; Excluir; confirmar.','Produto excluído com mensagem de sucesso.','Excluir Martelo com histórico.','Mensagem clara de bloqueio; produto e histórico preservados.'),
('6.1.6','Validar campos obrigatórios, limites textuais, peso não negativo e estoques inteiros não negativos; preservar dados e mostrar erros no topo e nos campos.','Salvar produto com valores válidos e peso zero.','Produto salvo; zero permitido.','Enviar marca com 61 caracteres, peso -1, estoque 1.5 e mínimo -2.','Erros visíveis por campo e no topo; entradas válidas preservadas.'),
('6.1.7','Retornar à interface principal a partir do cadastro.','Clicar Voltar à interface principal.','Painel autenticado aberto.','Após expiração da sessão, acessar o destino do botão.','Login solicitado.'),
('6.1.8','Exibir cadastro responsivo em português.','Abrir tabela e formulário em 390 px.','Formulário adaptado e tabela com rolagem horizontal.','Enviar dados inválidos em tela estreita.','Erros legíveis e ações continuam acessíveis.'),
('7.1.1','Listar estoque em ordem alfabética com algoritmo manual, ignorando caixa e acentos.','Criar nomes zebra, Árvore, alicate, Época e Borracha em base de teste e abrir estoque.','alicate, Árvore, Borracha, Época, zebra nessa ordem.','Executar ordenação sobre coleção vazia.','Coleção vazia retornada sem erro.'),
('7.1.2','Selecionar produto e escolher entrada ou saída por radio buttons.','Selecionar Martelo e Entrada.','Escolhas submetidas e movimento registrado.','Enviar tipo ajuste ou produto 999 inexistente.','Pedido rejeitado sem alteração de estoque ou histórico.'),
('7.1.3','Exigir data válida e não futura na movimentação.','Registrar com data de hoje.','Data armazenada e exibida no histórico.','Enviar amanhã ou 2026-02-30.','Data rejeitada sem registrar movimento.'),
('7.1.4','Alertar após saída abaixo do mínimo e destacar produtos críticos com badge vermelha.','Sair 8 unidades do Martelo (12 em estoque, mínimo 5).','Estoque 4, movimento salvo e alerta destacado com nome, saldo e mínimo.','Sair 7 unidades do Martelo (saldo 5).','Operação confirmada sem falso alerta de estoque mínimo.'),
('7.1.5','Exibir gestão de estoque limpa e responsiva.','Abrir estoque em 390 px.','Formulário, produtos e histórico legíveis.','Abrir tela sem produtos em base de teste.','Estado vazio legível, sem erro na página.'),
('7 adicional','Exigir quantidade inteira maior ou igual a 1 e bloquear saída superior ao estoque.','Sair exatamente 12 do Martelo.','Saldo zero e saída registrada com alerta.','Sair 13 do Martelo ou informar quantidade 0/1.5.','Erro claro; saldo e histórico não alterados.'),
('7 adicional','Registrar movimentação e saldo atomicamente, com trava de produto, responsável autenticado e proteção contra limite INT.','Ana registra entrada 3 no Martelo.','Saldo 15 e movimento de Ana, dentro da mesma transação.','Entrar 2147483647 unidades no Martelo.','Limite rejeitado e transação sem alterações.'),
('7 adicional','Exibir histórico com data, produto, tipo, quantidade e responsável, mais recentes primeiro e paginado.','Registrar entrada hoje e consultar histórico.','Nova entrada antes das antigas; todos os campos exibidos.','Abrir histórico em base de teste sem movimentações.','Nenhuma movimentação registrada; sem dados inventados.'),
('7 adicional','Retornar da gestão de estoque à interface principal.','Clicar Voltar à interface principal no estoque.','Painel aberto.','Acessar retorno com sessão encerrada.','Login solicitado.'),
('Segurança','Proteger as rotas, usar CSRF, hash bcrypt e escape do Blade.','Entrar com credenciais válidas e consultar formulário com token.','Login aceito e formulário contém token; senha no banco é bcrypt.','Enviar POST /estoque sem token em sessão real.','HTTP 419 e estoque inalterado.'),
]
doc('entrega01_requisitos_funcionais.md','# Entrega 01 - Requisitos funcionais\n\n'+ '\n'.join(f'- **RF{i:02} ({r[0]})**: {r[1]}' for i,r in enumerate(requisitos,1)))
doc('entrega08_casos_de_teste.md','''# Entrega 08 - Casos de teste

## 8.1 Casos positivos e negativos por requisito

Base: três usuários, quatro produtos e três entradas de 15/01/2026. Reiniciar a base de teste para cada caso; nunca reiniciar uma base real. Pré-condição padrão: sessão admin ativa e base inicial, exceto casos de login/visitante, que usam sessão encerrada. Casos vazios/nomes especiais usam base isolada. Os passos abaixo incluem os dados de entrada.

| ID | Requisito | Pré-condição | Passos e dados de entrada | Resultado esperado |
|---|---|---|---|---|
'''+ '\n'.join(f'| CT{i:02}{tipo} | RF{i:02} ({r[0]}) | {"Sem sessão" if i in [1,2] else "Base isolada; admin autenticado salvo indicação nos passos"} | {r[2] if tipo=="P" else r[4]} | {r[3] if tipo=="P" else r[5]} |' for i,r in enumerate(requisitos,1) for tipo in ['P','N'])+'''

## 8.2 Ferramentas e ambiente

- PHP 8.2.18, Laravel 11.57.0, PHPUnit 11.5.57.
- Testes Feature: `cd sistema` e `php artisan test`; SQLite em memória, explicitamente forçado em phpunit.xml. Não acessam saep_db.
- Integração local: MySQL 8.3.0, Windows 11 build 22631, WampServer, servidor Artisan na porta 8000.
- Navegador: Codex In-app Browser. Bootstrap 5.3.3 armazenado localmente.
- Casos de layout e CSRF devem ser verificados por navegador; o middleware CSRF é desabilitado pelo Laravel nos testes Feature.
- Resultados efetivamente executados estão em `verificacao.md`; a tabela acima descreve expectativas, não presume que todos os casos manuais foram executados.
''')
data=json.loads((s/'database/seeders/dados.json').read_text(encoding='utf-8'))
der='''# Entrega 02 - Diagrama entidade relacionamento

```mermaid
erDiagram
 usuario ||--o{ movimentacoes : realiza
 produtos ||--o{ movimentacoes : possui
 usuario {
  INT idusuario PK "AUTO_INCREMENT UNSIGNED"
  VARCHAR_100 name
  VARCHAR_100 email UK
  VARCHAR_255 password "bcrypt"
 }
 produtos {
  INT id PK "AUTO_INCREMENT UNSIGNED"
  VARCHAR_100 nome
  VARCHAR_60 marca
  VARCHAR_60 modelo
  VARCHAR_60 material
  VARCHAR_30 tamanho
  DECIMAL_8_2 peso
  VARCHAR_30 tensao
  INT estoque "default 0"
  INT estoque_minimo "default 0"
 }
 movimentacoes {
  INT id PK "AUTO_INCREMENT UNSIGNED"
  INT produto_id FK "UNSIGNED"
  INT usuario_id FK "UNSIGNED"
  ENUM tipo "entrada ou saida"
  INT quantidade
  DATE data_movimentacao
 }
```

Todas as colunas são NOT NULL. `usuario` guarda usuários autenticados; e-mail é único e senha é bcrypt. `produtos` descreve ferramentas, saldo atual e mínimo; peso é em kg. `movimentacoes` registra quantidade, tipo, data e responsável, sem timestamps. Cada movimento pertence obrigatoriamente a um usuário e um produto; cada um pode ter zero ou muitos movimentos. FKs usam ON DELETE RESTRICT e ON UPDATE CASCADE. INT UNSIGNED é usado para PKs e FKs compatíveis; continua sendo INT de 32 bits, não BIGINT. O PNG acompanha este diagrama.
'''
doc('entrega02_DER.md',der)
doc('entrega09_infraestrutura.md','''# Entrega 09 - Infraestrutura

| Item | Ambiente utilizado |
|---|---|
| SGBD | MySQL 8.3.0, InnoDB, utf8mb4 |
| Banco | saep_db, exatamente usuario, produtos e movimentacoes |
| Linguagem | PHP 8.2.18 |
| Framework | Laravel 11.57.0 |
| Front-end | Blade e Bootstrap 5.3.3, CSS local, sem build obrigatório |
| Sistema operacional | Windows 11, versão de kernel 10.0.22631 (23H2); edição não identificada |
| Servidor local | WampServer / PHP Artisan, 127.0.0.1:8000 |
| Testes | PHPUnit 11.5.57 e SQLite em memória |
| Extensões PHP | PDO, pdo_mysql, pdo_sqlite, mbstring, openssl, fileinfo, tokenizer, XML, ctype, curl |
| Dependências | Composer 2; instalar com composer.lock |

MySQL e PHP foram consultados no ambiente. O build do Windows foi lido por System.Environment.OSVersion; a edição não foi presumida. Não são necessários Node.js, Redis, filas externas ou acesso à internet para utilizar o sistema após instalar as dependências.
''')
readme='''# SAEP - Almoxarifado

Sistema do simulado SENAI, em português, com login manual, catálogo de ferramentas, entradas/saídas, alertas e histórico.

## Executar

O projeto nesta máquina já tem dependências, chave e banco inicializados. No PowerShell:

```powershell
cd C:\\wamp64\\www\\Saep\\sistema
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
- Quantidades são inteiras; saldo é protegido contra overflow INT. Peso limitado a DECIMAL(8,2). Datas futuras são avaliadas no fuso America/Sao_Paulo. Histórico ordenado por data decrescente e id decrescente, paginado em 20.
- Bootstrap 5.3.3 está em public/css; funciona sem CDN. `public` é a raiz web: nunca exponha a pasta do projeto ou .env no Apache.
- Laravel 11 é a versão exigida, embora o Composer tenha informado advisories para ela neste ambiente. A instalação inicial usou `--no-security-blocking` para cumprir o simulado local. Antes de uso real, atualizar framework/dependências e trocar credenciais de demonstração. O ZIP conserva composer.lock para instalação reproduzível.

## Ordenação

`app/Services/OrdenacaoService.php` implementa Insertion Sort estável sobre `Produto::all()`. Normaliza com mb_strtolower e transliteração Str::ascii; compara chaves e desloca elementos manualmente. Não usa orderBy, sort, usort ou sortBy na listagem de produtos do estoque. Custo médio/pior O(n²), melhor O(n), memória auxiliar O(1) para ordenar o array, além da coleção/array recebido. Foi escolhido por ser simples de explicar e adequado ao pequeno catálogo do simulado. A normalização também depende do comprimento dos nomes, limitado a 100 caracteres.

## Arquivos de entrega

`entregas/` contém requisitos, DER em Mermaid e PNG, SQL, casos de teste e infraestrutura. `Aluno_SAEP.zip` reúne esses documentos e `sistema/` sem vendor, node_modules, .env, caches ou logs. O README também está dentro do sistema e na raiz do ZIP.

## Checklist do caderno

'''
implementacao=['AuthController e auth/login','auth/login e layouts/app','home e layouts/app','AuthController::logout e layouts/app','home → produtos.index','home → estoque.index','home e app.css','ProdutoController::index e produtos/index','Produto::scopeBuscar e produtos/index','ProdutoController::store e produtos/form','ProdutoController::update e produtos/form','ProdutoController::destroy e confirmação em produtos/index','ProdutoRequest, produtos/form e x-alertas','produtos/index e produtos/form','produtos/*, Bootstrap e app.css','OrdenacaoService e EstoqueController::index','estoque/index e MovimentacaoRequest','MovimentacaoRequest e estoque/index','EstoqueController::registrar, x-alertas e badge','estoque/index, Bootstrap e app.css']
readme+='\n'.join(f'- [x] {r[0]} — {r[1]} Implementação: `{impl}`.' for r,impl in zip(requisitos[:20],implementacao))
readme+='\n\nConsulte `entregas/verificacao.md` para resultados de execução, importação e testes.\n'
(root/'README.md').write_text(readme,encoding='utf-8');(s/'README.md').write_text(readme,encoding='utf-8')
# DER estático de alta resolução com campos e cardinalidades explícitas.
im=Image.new('RGB',(1800,1100),'#f3f6f9');d=ImageDraw.Draw(im)
font='C:/Windows/Fonts/segoeui.ttf';bold='C:/Windows/Fonts/segoeuib.ttf'
f=ImageFont.truetype(font,23);fb=ImageFont.truetype(bold,30);title=ImageFont.truetype(bold,40)
d.text((70,40),'SAEP • Diagrama entidade relacionamento',font=title,fill='#102d43')
boxes=[('usuario',(70,180,555,530),['PK idusuario INT UNSIGNED AI','name VARCHAR(100)','UK email VARCHAR(100)','password VARCHAR(255)']),('produtos',(70,650,650,1045),['PK id INT UNSIGNED AI','nome VARCHAR(100)','marca / modelo / material VARCHAR(60)','tamanho / tensao VARCHAR(30)','peso DECIMAL(8,2)','estoque / estoque_minimo INT DEFAULT 0']),('movimentacoes',(1010,370,1725,825),['PK id INT UNSIGNED AI','FK produto_id INT UNSIGNED → produtos.id','FK usuario_id INT UNSIGNED → usuario.idusuario',"tipo ENUM('entrada','saida')",'quantidade INT','data_movimentacao DATE'])]
for name,box,fields in boxes:
 x,y,x2,y2=box;d.rounded_rectangle(box,15,fill='white',outline='#9bb2c0',width=2);d.rectangle((x+1,y+1,x2-1,y+63),fill='#102d43');d.text((x+20,y+12),name,font=fb,fill='white')
 for j,line in enumerate(fields):d.text((x+20,y+90+j*43),line,font=f,fill='#172d40')
d.line([(555,355),(790,355),(790,525),(1010,525)],fill='#087e8b',width=5)
d.text((595,315),'1',font=fb,fill='#087e8b');d.text((910,480),'0..N',font=fb,fill='#087e8b')
d.line([(650,840),(825,840),(825,720),(1010,720)],fill='#087e8b',width=5)
d.text((690,850),'1',font=fb,fill='#087e8b');d.text((915,675),'0..N',font=fb,fill='#087e8b')
d.text((1040,920),'Todas as colunas: NOT NULL',font=f,fill='#526678');d.text((1040,960),'FKs: DELETE RESTRICT / UPDATE CASCADE',font=f,fill='#526678');d.text((1040,1000),'Sem timestamps • Peso em kg • AI = auto incremento',font=f,fill='#526678')
im.save(e/'entrega02_DER.png')
print('Documentação e DER gerados.')
