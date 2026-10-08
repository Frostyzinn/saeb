from pathlib import Path
import json,zipfile
root=Path(__file__).resolve().parents[1];s=root/'sistema';e=root/'entregas'
for path in ['resources/views/welcome.blade.php','resources/css/app.css','resources/js/app.js','resources/js/bootstrap.js','package.json','vite.config.js','tailwind.config.js','postcss.config.js','database/database.sqlite']:
 (s/path).unlink(missing_ok=True)
(e/'verificacao.txt').unlink(missing_ok=True)
c=s/'composer.json';dados=json.loads(c.read_text(encoding='utf-8'));dados['description']='Sistema de almoxarifado do simulado SAEP';dados['scripts']['dev']=['Composer\\Config::disableProcessTimeout','@php artisan serve'];dados['scripts']['post-create-project-cmd']=['@php artisan key:generate --ansi'];c.write_text(json.dumps(dados,ensure_ascii=False,indent=4)+'\n',encoding='utf-8')
for p in [root/'README.md',s/'README.md']:
 t=p.read_text(encoding='utf-8').replace('Quantidades são inteiras;', 'As migrations fixam InnoDB explicitamente, pois o padrão do Wamp desta máquina era MyISAM; assim as FKs, transações e travas funcionam. Quantidades são inteiras;')
 p.write_text(t,encoding='utf-8')
(e/'verificacao.md').write_text('''# Verificação da entrega

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
''',encoding='utf-8')
def pack():
 with zipfile.ZipFile(root/'Aluno_SAEP.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in e.iterdir():
   if p.is_file():z.write(p,'Aluno_SAEP/'+p.name)
  z.write(root/'README.md','Aluno_SAEP/README.md')
  for p in s.rglob('*'):
   rel=p.relative_to(s);parts=rel.parts
   if any(x in parts for x in ['vendor','node_modules','.git']):continue
   if not p.is_file():continue
   if p.name in ['.env','.phpunit.result.cache']:continue
   if (parts[0]=='storage' or parts[:2]==('bootstrap','cache')) and p.name!='.gitignore':continue
   z.write(p,'Aluno_SAEP/sistema/'+rel.as_posix())
  for d in ['storage/app/private','storage/app/public','storage/framework/cache/data','storage/framework/sessions','storage/framework/views','storage/logs','bootstrap/cache']:
   z.writestr('Aluno_SAEP/sistema/'+d+'/',b'')
 with zipfile.ZipFile(root/'Aluno_SAEP.zip') as z:
  assert z.testzip() is None
  assert not any('/vendor/' in n or '/node_modules/' in n or n.endswith('/.env') for n in z.namelist())
  print(f'ZIP verificado: {len(z.namelist())} arquivos/entradas, {(root/"Aluno_SAEP.zip").stat().st_size} bytes')
if __name__=='__main__':pack()
