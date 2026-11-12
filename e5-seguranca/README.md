# Entrega 5 - Captura e cartilha de Wi-Fi seguro

**Esta entrega e INDEPENDENTE da E4.** No site do professor, escolha **Entrega 5 - Captura e Cartilha**. Nota de Extensao, de 0 a 2,0 pontos.

## Laboratorio isolado
Este repositorio possui tres contêineres proprios: cliente (`10.0.10.10`), roteador (`10.0.10.254` / `10.0.20.254`) e servidor (`10.0.20.20`). As capturas ocorrem exclusivamente na interface interna do roteador, em requisicoes geradas pelo proprio cliente para o proprio servidor. **Nao capture trafego da faculdade, de Wi-Fi publico ou de outras pessoas.**

O servidor publica HTTP em 8080 e TLS em 8443 usando certificado autoassinado somente para demonstracao. **Jamais ignore alertas de certificado em um site real.** O token do teste e didatico, nao uma senha verdadeira.

## Identificador
`token.txt` usa provisoriamente `GRUPO-LUIZ-FERNANDO-1055368-1`, vinculado ao responsavel do repositorio. Se houver outros integrantes ou outro identificador oficial, substitua antes de fazer a captura final.

## Verificacao / geracao das capturas
Na raiz do repositorio, com Docker e Docker Compose:
```bash
make up E=5
make evidencias E=5
make down E=5
```
O verificador `verificar.sh` foi copiado sem alteracoes do laboratorio oficial do professor.

O teste deve confirmar: token proprio; acesso HTTP; token visivel em HTTP; trafego HTTPS nao vazio; token invisivel no HTTPS. **Somente apos verificacao verde** devem ser usados os arquivos reais:
- `claro.pcap` - captura HTTP do laboratorio
- `cifrado.pcap` - captura HTTPS do laboratorio
- `evidencias/verificacao.txt` - resultado do verificador

O fluxo GitHub Actions `Gerar evidencias E5` roda a mesma topologia Docker isolada, executa o verificador e, se passar, publica capturas reais na pasta E5. Ele tambem monta `cartilha.pdf` a partir dos dados da captura. Confira a execucao e o resultado antes de enviar.

## Cartilha e comprovacao de extensao
- `cartilha.pdf`: cartilha gerada a partir da captura verdadeira, nao de imagem da internet.
- `evidencias/trecho-captura-http.txt`: texto extraido de `claro.pcap` para montar a imagem central.
- **Aprimoramento recomendado:** abrir `claro.pcap` no Wireshark, usar Seguir fluxo TCP, obter um print real da linha `Authorization: Bearer...` e substituir o painel da cartilha por esse print para aderencia literal ao enunciado.
- Para **1,7**: apresentar a publico real fora da sala e anexar registro autentico.
- Para **2,0**: incluir numero real de pessoas, perguntas que fizeram e cartilha efetivamente revisada depois do retorno. Nao inventar registro nem feedback.

## Entrega pelo site
URL: https://github.com/luizf23-star/lab-redes
Selecione **Entrega 5 - Captura e Cartilha** e anexe `cartilha.pdf`, `claro.pcap`, `cifrado.pcap`. Envie evidencias de apresentacao e retorno apenas se realmente ocorreram.

[Enunciado oficial](https://github.com/LuizRMSilva1973/redes-lab/blob/main/entregas/E5.md)
