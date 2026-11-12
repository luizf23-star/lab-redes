# Senha sem cadeado: entenda o risco (texto-base da cartilha)

Este texto orienta a cartilha visual `cartilha.pdf`, gerada APOS executar a captura propria do laboratorio.

## O que aconteceu no nosso laboratorio
Fizemos duas conexoes entre maquinas sob nosso controle, dentro de uma rede isolada. Na pagina HTTP (sem protecao), o nosso segredo inventado apareceu legivel durante a captura. Na versao HTTPS, observamos trafego, mas o mesmo segredo nao apareceu de forma legivel.

**Imagem central obrigatoria:** retirada da captura `claro.pcap` deste repositorio. Nao usar imagem da internet nem material de outro grupo.

## Como reconhecer no celular
Toque no icone ao lado do endereco do site (pode ser cadeado ou um simbolo de controles, dependendo do navegador) e consulte as informacoes da conexao. Confira se o endereco comeca por `https://` e se o navegador nao exibe aviso de conexao insegura ou erro de certificado. HTTPS nao garante, sozinho, que o site seja verdadeiro: confira tambem o endereco.

## Tres atitudes concretas
1. Se o site disser "Nao seguro" ou avisar erro de certificado, NAO digite sua senha. Feche e encontre o endereco oficial.
2. Em Wi-Fi publico, prefira sua internet movel para acessar banco, e-mail e outras contas importantes. Se usar a rede publica, confira o endereco e a protecao do site.
3. Se voce ja digitou senha em uma pagina suspeita, troque-a acessando o site oficial e ative a verificacao em duas etapas.

## Observacao sobre nosso teste
Usamos uma senha inventada em maquinas proprias. O HTTPS do laboratorio usa certificado criado por nos mesmos, por isso o navegador reclamaria; o teste automatizado ignora essa reclamacao SO no ambiente controlado. Em sites reais, nunca ignore esse aviso.

## Extensao ao publico
Anotar apenas fatos ocorridos: numero de participantes, data, local, perguntas autenticas e alteracoes de conteudo feitas apos ouvir o publico. Guardar foto, lista ou gravacao com consentimento.
