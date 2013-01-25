TODO
====

6. Comentários (hierarquia / relacionamento)
7. Gravacao e consula de rating (caso de alta freqüencia de escrita)
8. Busca de softwares relacionados por ordem de download

---

1. Consultas
  ✓ reviews de softwares de uma categoria específica (e.g.== S.O.) ordenada por contagem de comentários
  
  <cypher>
        
        START r=node:reviews("slug:*") 
        MATCH r-[:revises]->()-[:in_category]->c, m-[:has_context]->r  
        WHERE c.slug="\"SO\"" 
        RETURN r,count(m) 
        ORDER BY count(m) DESC;

  </cypher>    


   <sparql>

        PREFIX s: <http://semantica.globo.com/tech/schemas/>
        PREFIX cat: <http://semantica.globo.com/tech/software-categories/>
 
        select (count(?comment) as ?commentCount) ?review  from <http://mythical_poc.globo.com/tech/> 
        {
          ?review   a               s:SoftwareReview .
          ?review   s:revises       ?software .
          ?review   s:has_comment   ?comment .
          ?software s:in_category   cat:OperatingSystem .
        } 
        ORDER BY DESC(?commentCount)    

   </sparql>
   
   
  ✓ listagem de linguagens de query suportadas 
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

Idéias sobre a API de Dados
===========================
   - Devem existir namespaces, de forma que os dados/esquemas sejam definidos no contexto destes namespaces
   - JSON é formato básico de representação de dados
