import networkx as nx
import matplotlib.pyplot as plt

# Nome do arquivo GML que você baixou do Topology Zoo
gml_file = 'Ans.gml'

try:
    # Carrega o grafo diretamente do arquivo GML
    G = nx.read_gml(gml_file, label='id') # O 'label' pode variar dependendo do arquivo GML

    # --- Contagem de Nós e Links ---
    num_nodes = G.number_of_nodes()
    num_links = G.number_of_edges()

    print(f"Grafo '{gml_file}' carregado com sucesso!")
    print(f"O grafo tem {num_nodes} nós.")
    print(f"O grafo tem {num_links} links.")

    # Mostra os nós e arestas (opcional)
    # print("\nNós:", G.nodes())
    # print("Links:", G.edges())

    # --- Visualização do Grafo (Opcional) ---
    plt.figure(figsize=(10, 8))
    # 'pos' pode não ser definido no GML, mas o networkx vai calcular uma posição
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', font_size=10)
    plt.title("Visualização do Grafo a partir de GML")
    plt.show()

except FileNotFoundError:
    print(f"Erro: O arquivo '{gml_file}' não foi encontrado.")
    print("Por favor, baixe o arquivo .gml do Topology Zoo e coloque-o no mesmo diretório deste script.")

except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo GML: {e}")
