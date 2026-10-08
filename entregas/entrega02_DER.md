# Entrega 02 - Diagrama entidade relacionamento

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
