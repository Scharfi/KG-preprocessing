
import org.aksw.jena_sparql_api.core.QueryExecutionFactory;
import org.aksw.jena_sparql_api.http.QueryExecutionFactoryHttp;
import org.apache.jena.query.*;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;

import java.io.*;
import java.util.List;

public class constructer {

    public static void main(String[] args)
            throws Exception {
        // Create a query execution over my data
        QueryExecutionFactory qef = new QueryExecutionFactoryHttp("http://localhost:3030/sparqlhost_data/sparql", "https://www.lidl.de/de/");
        QueryExecutionFactoryHttp foo = qef.unwrap(QueryExecutionFactoryHttp.class);
        System.out.println(foo);


        // Create a QueryExecution object from a query string: && ?p != <http://dice-researcher.com/grocery-recommendation/customer#list> && ?p != <http://projekt-opal.de/dataset#pagination>
        String queryString = "CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o . FILTER (?p != <http://dice-researcher.com/grocery-recommendation/customer#list> && ?p != <http://dice-researcher.com/grocery-recommendation/recommendation#list && ?p != <http://dice-researcher.com/dataset#pagination>).}";
        //String queryString = "SELECT DISTINCT ?s WHERE { ?s ?p ?o . FILTER(?p!=<http://dice-researcher.com/grocery-recommendation/recommendation#list> && ?p != <http://dice-researcher.com/grocery-recommendation/customer#list> && ?p != <http://projekt-opal.de/dataset#pagination>).}";

        //String queryString = "SELECT DISTINCT ?s ?p ?o  WHERE {   \n" +
        //        "    ?s ?p ?o . FILTER(?p=<http://dice-researcher.com/title> || ?p=<http://dice-researcher.com/description> ||?p=<http://dice-researcher.com/grocery-recommendation/properties> || "+
        //        "?p=<http://dice-researcher.com/grocery-recommendation/careinstructions> || ?p=<http://dice-researcher.com/grocery-recommendation/material> || ?p=<http://dice-researcher.com/grocery-recommendation/technicalDetails> || ?p=<http://dice-researcher.com/grocery-recommendation/delivery> || ?p=<http://dice-researcher.com/grocery-recommendation/color> || ?p=<http://dice-researcher.com/grocery-recommendation/wine#attributes> || ?p=<http://dice-researcher.com/grocery-recommendation/spirits#attributes> )  .}";



        //Simple Select save as CSV
        /*Query query = QueryFactory.create(queryString);
        QueryExecution qe = qef.createQueryExecution(query);
        ResultSet results = qe.execSelect();
        FileOutputStream o = new FileOutputStream(new File("ConexData.txt"));
        //ResultSetFormatter.out(o,results);
        ResultSetFormatter.outputAsCSV(o, results);
        */

        // Construct graph
        Query query = QueryFactory.create(queryString, Syntax.syntaxSPARQL_11);
        QueryExecution q = qef.createQueryExecution(query);
        Model result = q.execConstruct();
        String fileName = "dataset.owl";
        FileWriter out = new FileWriter(fileName);
        //RDFDataMgr.write(System.out, result, RDFFormat.TURTLE) ;
        //result.write(System.out, "N-TRIPLES");

        try {
            result.write(out, "RDF/XML");
        } finally {
            try {
                out.close();
            } catch (IOException closeException) {
                // ignore
            }

        }

    }
}


