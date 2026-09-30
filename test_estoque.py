from ward import test, fixture, raises

from estoque import Estoque, ProdutoNaoEncontrado, EstoqueInsuficiente
from carrinho import Carrinho

@fixture
def estoque_com_canetas():
    e = Estoque()
    e.adicionar_produto("Caneta", 10)
    return e

"""Teste de Unidade: Testam partes específicas do código"""
@test("UNIDADE - adicionar produto novo cria o item com a quantidade correta")
def _():
    estoque = Estoque()
    estoque.adicionar_produto("Caderno", 20)
    assert estoque.consultar_quantidade("Caderno") == 20

@test("UNIDADE - adicionar produto existente soma com a quantidade atual")
def _(estoque=estoque_com_canetas):
    estoque.adicionar_produto("Caneta", 5)
    assert estoque.consultar_quantidade("Caneta") == 15

@test("UNIDADE - remover quantidade correta diminui o estoque corretamente")
def _(estoque=estoque_com_canetas):
    estoque.remover_produto("Caneta", 4)
    assert estoque.consultar_quantidade("Caneta") == 6

@test("UNIDADE - adicionar quantidade zero ou negativa é rejeitado")
def _():
    estoque = Estoque()
    with raises(ValueError):
        estoque.adicionar_produto("Lápis", 0)

@test("UNIDADE - remover mais do que o disponível gera EstoqueInsuficiente")
def _(estoque=estoque_com_canetas):
    with raises(EstoqueInsuficiente):
        estoque.remover_produto("Caneta", 999)

@test("UNIDADE - consultar produto que não exist gera ProdutoNaoEncontrado")
def _():
    estoque = Estoque()
    with raises(ProdutoNaoEncontrado):
        estoque.consultar_quantidade("Borracha")

"""Nessa parte do código está o bug que foi falado no Slide!"""
@test("UNIDADE BUG - remover quantidade negativa deveria ser rejeitada")
def _(estoque=estoque_com_canetas):
    with raises(ValueError):
        estoque.remover_produto("Caneta", -5)
    """
    O Teste acha o comportamento correto, porque na validação quantidade > disponivel nunca é True, então qualquer número que for colocado contato que seja inteiro, será válido, e o estoque acaba aumentando em vez de rejeitar, isso é um bug do metodo remover_produtos().
    """

"""Testes de Integração - Testam conexões de uma parte do código com outra, nesse caso, do Carrinho com Estoque """
@test("INTEGRAÇÃO - adicionar item no carrinho reserva a quantidade no estoque")
def _(estoque=estoque_com_canetas):
    carrinho = Carrinho(estoque)
    carrinho.adicionar_item("Caneta", 3)

    assert carrinho.total_itens() == 3
    assert estoque.consultar_quantidade("Caneta") == 7  # 10 - 3

@test("INTEGRAÇÃO - comprar dois produtos diferentes atualiza o estoque dos dois produtos")
def _():
    estoque = Estoque()
    estoque.adicionar_produto("Caneta", 10)
    estoque.adicionar_produto("Caderno", 5)

    carrinho = Carrinho(estoque)
    carrinho.adicionar_item("Caneta", 2)
    carrinho.adicionar_item("Caderno", 1)

    assert carrinho.resumo() == {"Caneta": 2, "Caderno": 1}
    assert estoque.consultar_quantidade("Caneta") == 8
    assert estoque.consultar_quantidade("Caderno") == 4


@test("INTEGRAÇÃO - tentar comprar mais do que o estoque tem é bloqueado")
def _(estoque=estoque_com_canetas):
    carrinho = Carrinho(estoque)
    with raises(EstoqueInsuficiente):
        carrinho.adicionar_item("Caneta", 50)

    assert estoque.consultar_quantidade("Caneta") == 10
"Estoque continua com a mesma quantidade de sempre, já que ele foi bloqueado"