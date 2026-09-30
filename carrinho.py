from estoque import Estoque

class Carrinho:
    """Carrinho faz integração com Estoque: quando adicionamos um item
    no carrinho, a quantidade do item no carrinho é retirada do estoque."""
    def __init__(self, estoque: Estoque):
        self._estoque = estoque
        self._itens = {}

    def adicionar_item(self, nome: str, quantidade: int):
        self._estoque.remover_produto(nome, quantidade)
        self._itens[nome] = self._itens.get(nome, 0) + quantidade

    def total_itens(self) -> int:
        return sum(self._itens.values())

    def resumo(self) -> dict:
        return dict(self._itens)
