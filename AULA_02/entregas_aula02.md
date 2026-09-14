João Vitor da Silva Batista, Juan Pablo Santana Macedo Curso: CDC6

Sobre o estado do robô e a pose 2D: a pose representa a posição e a direção do robô, com três valores — x, y e theta.
O x e o y indicam onde o robô está, enquanto o theta mostra para qual direção ele está virado. A orientação importa porque, mesmo estando no mesmo lugar, 
um robô apontado para direções diferentes se move de formas diferentes no passo seguinte.
Sobre a cinemática diferencial: o robô tem duas rodas independentes, uma de cada lado, e a diferença entre as velocidades delas determina como ele se movimenta. 
Quando as duas rodas giram na mesma velocidade, o robô anda reto. Quando uma roda está mais rápida que a outra, ele faz uma curva. E se as rodas girarem em sentidos opostos
(v_R = -v_L), o robô gira em torno do próprio eixo sem sair do lugar — foi o que testamos no Exercício 1 segurando W e K juntos. Também testamos o caso de travar uma roda (v_R = 0, v_L > 0),
em que o robô gira em torno da roda parada em vez de girar no próprio centro, segurando só a tecla W.
Sobre a odometria discreta: é a forma de estimar a posição do robô a partir do seu próprio movimento — velocidade das rodas e tempo — sem depender de nenhum sensor externo.
É chamada de discreta porque o cálculo é feito em pequenos intervalos de tempo fixos, e não de forma contínua. Como a posição é recalculada passo a passo, pequenos erros aparecem a cada passo[...]
No Exercício 2 isso ficou claro: depois de percorrer o quadrado, o robô não voltou exatamente ao ponto de partida. No nosso teste, o erro final foi de cerca de 10,6 px de distância e 3,9° de [...]
Sobre a navegação GO-TO-GOAL: é uma técnica para fazer o robô chegar até um ponto determinado. Primeiro ele calcula a direção do alvo e compara com sua orientação atual; a partir dessa diferença[...]
Quanto maior o erro de direção, maior a correção aplicada — por isso chamamos de controlador proporcional. Um cuidado que tivemos na implementação foi normalizar esse erro de ângulo: sem isso, o robô confundia +170° com -170°,[...]
quando na prática ele só precisava girar -20° no sentido contrário. Quando o robô fica a menos de 10 pixels do alvo, ele para.
Em resumo, os exercícios ajudaram a entender como o robô representa sua posição, como as rodas controlam o movimento e como ele consegue navegar até um destino. Também vimos na prática que odometria não é perfeita,[...]
relevante em robótica móvel real, onde o robô não tem como "resetar" sua posição sem um sensor externo.