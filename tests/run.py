from app.node import Node
from app.blockchain import BlockchainPoS

if __name__ == "__main__":
    # Cria uma instância da BlockchainPoS
    blockchain = BlockchainPoS()

    # Passa a blockchain para o Node
    node = Node(blockchain)

    # Inicia o servidor Flask
    node.app.run( debug=True,host='0.0.0.0', port=5070)
