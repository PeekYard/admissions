# Peekyard — Admissão de projetos (MVP, Etapa 1)

Este repositório público recebe pedidos para exibir landing pages na vitrine [Peekyard](https://peekyard.com). O pedido é um **GitHub Issue público** e contém endereço de um repositório-fonte público do criador.

**Escopo restrito:** triagem e avaliação consultiva. Nenhum workflow cria repositórios, concede permissões, faz merge ou publica páginas.

## Configuração

1. Revise e faça merge do PR de implantação na branch principal.
2. Confirme que Issues e GitHub Actions estão habilitados nas configurações deste repositório.
3. Teste o formulário em https://github.com/PeekYard/admissions/issues/new/choose .
4. Criar um Issue válido dispara o workflow Admissão · triagem técnica, que escreve um comentário automático e um rótulo:
   - admission:triaged — campos validados; **não significa aprovação**.
   - admission:needs-info — há pendências.
5. Para reanalisar após uma edição de Issue, PeekYardMaster acessa Actions → Admissão · triagem técnica → Run workflow e informa o número do Issue.
6. Recomenda-se que PeekYardMaster use Watch → All activity e habilite as notificações de e-mail no GitHub.

## Análise por IA — opcional e paga separadamente

1. Crie uma chave da **OpenAI API** e guarde-a em Settings → Secrets and variables → Actions → Repository secrets, com o nome OPENAI_API_KEY. Nunca publique a chave em texto ou Issue.
2. Opcionalmente, configure a variável OPENAI_MODEL em Settings → Secrets and variables → Actions → Variables. O modelo padrão proposto é gpt-5-mini (verifique disponibilidade e preços na conta).
3. Após triagem, **PeekYardMaster** adiciona manualmente ao Issue o rótulo admission:run-ai.
4. O workflow de IA somente executa quando o rótulo é aplicado por GitHub user ID 349365411. O parecer é adicionado ao Issue e **não aprova nem rejeita automaticamente**.
5. Para repetir a análise, remova o rótulo e aplique-o novamente.
6. A API recebe amostras limitadas de código-fonte público, políticas e dados de formulário. Ela pode falhar, alucinar e sofrer tentativas de prompt injection. A revisão humana é obrigatória.

## Segurança

- A triagem lê dados públicos pela API GitHub, com limites de tamanho e número de arquivos. **Não clona, instala pacotes nem executa código de terceiros**.
- A URL de origem deve pertencer à conta GitHub que abriu o Issue. Isto não comprova titularidade da marca, autoria ou propriedade intelectual.
- É registrado um commit SHA para orientar revisões futuras. O código pode mudar depois do relatório; antes de publicar, será obrigatória uma nova verificação do SHA aprovado.
- Os workflows que recebem Issues públicos usam somente permissões limitadas (contents: read e issues: write) e **nenhum token de provisionamento**.
- Arquivos de governança de projetos, scripts externos, CDNs e uso de storage da origem são sinalizados para análise aprofundada.
- Como os projetos em peekyard.com/caminho compartilham a mesma origem, **JavaScript arbitrário não pode ser considerado isolado somente pela revisão estática ou por IA**. Precisaremos definir isolamento de origem na etapa de publicação.
- O GitHub Issues é público: não publicar senhas, dados pessoais sensíveis ou informações sigilosas.
- Não habilitar ações de publicação ou gestão de acessos neste repositório durante a Entrega 1.

## Políticas

- policies/eligibility.md — requisitos mínimos.
- policies/content.md — critérios editoriais e proibições.
- policies/security.md — segurança técnica e limites de avaliação.

## Fluxo

Formulário → Issue → triagem automática → relatório + rótulo → revisão administrativa → (opcional) parecer de IA sob acionamento manual.

A criação de repositórios e a publicação serão implementadas nas Entregas 2 e 3, respectivamente.

## Testes

Execute localmente:

    python3 -m unittest discover -s tests -v

### Limitações conhecidas

Este scanner usa heurísticas e amostras (até 50 arquivos, 512 KiB totais), não oferece garantia contra malware, nem faz avaliação completa de dependências em tempo de execução. Formulários podem ser editados depois do relatório, sem reprocessamento automático; solicite reanálise manual. A avaliação da IA é consultiva. Repositórios pertencentes a organizações externas não são admitidos automaticamente nesta primeira versão.
