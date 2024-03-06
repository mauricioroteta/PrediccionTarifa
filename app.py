import streamlit as st 

#Definir el título
st.title('Mi primer app')

st.write("Esta aplicación tiene el objetivo de elevar cualquier número al cuadrado:")

x = st.number_input('Introduzca un número:')

st.write('El número al cuadrado es:', x**2)


def card():
    return """
        <div class="card" style="width: 18rem;">
        <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
        </div>
    """

st.write(card())

var1 = st.sidebar.slider('Hola', 13, 78, 10)