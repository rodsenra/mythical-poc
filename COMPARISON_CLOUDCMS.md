# CloudCMS

## Types (análogo aos nossos Schemas)

http://code.cloudcms.com/javascript-samples/#/components/node-type

## Nodes (análogo às nossas Instâncias)

http://code.cloudcms.com/javascript-samples/#/components/node

## Associations

http://code.cloudcms.com/javascript-samples/#/components/node-association

Obs.:

No nossa POC, as associations foram criadas simultâneamente e automaticamente baseadas nos schemas pois são associações obrigatórias. Ex.: não existe review sem software. Mas na nossa implementação definitivamente tb teremos cadastro de associações adhoc.

## Consulta

http://code.cloudcms.com/javascript-samples/#/components/node

http://code.cloudcms.com/javascript-samples/#/components/node-traverse

Mas na nossa POC, fazemos um GET para a URI de um Review e obtemos um JSON expandido contendo o Review e seus nós de primeiro nível (Software e Commments).
