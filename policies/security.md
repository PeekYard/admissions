# Política de segurança de landing pages (v1)

Autores têm liberdade de template, mas cada mudança precisa de revisão e aprovação explícita antes de produção.

- Scripts inline, JavaScript próprio, iframes, serviços externos e CDNs não são automaticamente proibidos, mas exigem avaliação de risco.
- Dependências externas podem mudar depois da revisão: preferir versões fixas, SRI quando aplicável e fontes confiáveis.
- O código fonte do solicitante jamais será executado pela triagem ou análise contextual. Não executar builds, `npm install`, scripts ou workflows desse repositório em runners privilegiados.
- Bloquear eventual publicação se a análise estiver incompleta, o commit tiver mudado ou houver risco não resolvido.
- Arquivos como `CNAME`, `.github/workflows/**`, `.github/CODEOWNERS` e scripts de provisionamento são governança exclusiva da Peekyard.
- Não aceitar chaves privadas, tokens, dados pessoais sensíveis, programas maliciosos, mineração oculta, roubo de credenciais ou uso não autorizado da marca Peekyard.
- Cuidado: `https://peekyard.com/projeto-a/` e `https://peekyard.com/projeto-b/` compartilham a mesma origem no navegador. Nenhuma análise estática ou de IA garante isolamento. Antes de publicar JS arbitrário, é necessário decidir e aplicar controles de origem (ex.: subdomínios isolados).
- A triagem não substitui testes em sandbox isolada, revisão humana e monitoramento de dependências.
