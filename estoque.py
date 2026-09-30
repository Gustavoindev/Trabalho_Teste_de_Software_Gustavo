class ProdutoNaoEncontrado(Exception):
    pass
class EstoqueInsuficiente(Exception):
    pass

class Estoque:
    
    def __init__(self):
        self._produtos = {}

    def adicionar_produto(self, nome: str, quantidade: int):
        if quantidade <= 0:
            raise ValueError("A quantidade selecionada deve ser maior que zero")
        self._produtos[nome] = self._produtos.get(nome, 0) + quantidade

    def consultar_quantidade(self, nome: str) -> int:
        if nome not in self._produtos:
            raise ProdutoNaoEncontrado(f"Produto '{nome}' não está no estoque")
        return self._produtos[nome]

    def remover_produto(self, nome: str, quantidade: int):
        if nome not in self._produtos:
            raise ProdutoNaoEncontrado(f"Produto '{nome}' não está no estoque")

        disponivel = self._produtos[nome]

        """ Parte do código "Bugada": não faz a validação se 'quantidade' for positiva.
            Se for um número negativo, a subtração aumenta no estoque em vez de rejeitar a operação.
        """
        if quantidade > disponivel: 
            raise EstoqueInsuficiente(
                f"Estoque insuficiente de '{nome}': quanatidade disponível {disponivel}, solicitado {quantidade}"
            )
        self._produtos[nome] -= quantidade
