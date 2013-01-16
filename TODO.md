TODO
====

6. Comentários (hierarquia / relacionamento)
7. Gravacao e consula de rating (caso de alta freqüencia de escrita)
8. Busca de softwares relacionados por ordem de download

---

1. Consultas
  ✓ review de 1 dada categoria ordenada por contagem de cometários
  ✓ listagem de lingaugens de query suportadas 
  ✓ consulta textual restrita a um tipo
  ✓ dado comentário recuperar caminho de comments até review
     start n=node(44) match n-[:replies*]->t-[:has_context]->x return  n, t, x;
  ✓ dado software obter todos reviews
     g.v(18).inE.filter{it.label=="revises"}.outV.map
     start n=node(18) match n<-[:revises]-x return x;
      
2. ✓ Vínculo "amarrado" content-review

3. Estudo de semântica
   -  Exercício com SPARQL/Virtuoso

4. Interface CMA->(Dados + Semantica)

5. Tecnologia para Stack da API (definir critérios)

6. Bechmarks de DB's (critérios)

7. Suporte a ratings (acesso real-time, fast counters, analytics)

8. Discutir formato do JSON de recuperação de dados 
   - embeded vs linked daat structures
   - representar incoming + outgoing links

