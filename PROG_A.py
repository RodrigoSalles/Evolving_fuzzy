""" Programa A """


""" Carregar bibliotecas """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import time


""" Iniciar variáveis """
cluster_dict = {} # Dicionário par aarmazenar thetas, de acordo com cluster.
theta_evolving = []
novelty_threshold = 0.3
merge_threshold = 0.8
y = 40
initial_theta = 0
clusters = []
centers = []
covariances = []
Lambdas = []
thetas = []
updated_clusters = []
theta_history = []
feature = 'TSS'


""" Função para plotar gráfico dos thetas, por cluster. """
def grafico(cluster_dict, cluster_num, novo_theta):
    # Verificar se o cluster já existe
    if cluster_num not in cluster_dict:
        # Criar um novo vetor para o novo cluster
        cluster_dict[cluster_num] = []

    # Atualizar o valor de theta para o cluster especificado
    cluster_dict[cluster_num].append(novo_theta)



""" Função para criar dataset menor, para testes. """
def sample_dataset(df_p1, df_p2, number_of_rows):
    df1_testes = df_p1.head(number_of_rows)
    df2_testes = df_p2.head(number_of_rows)
    return df1_testes, df2_testes

""" Função para normalizar dados e transformar em array. Essa função recebe as 
amostras em streaming. """
def normalise(sample):
    norm_vector = scaler.transform(sample.values.reshape(1, -1)).T
    return norm_vector

""" Carregar normalizador """
scaler = joblib.load('C:/Users/User/Desktop/PROG_A/scaler.joblib')

""" Inicializar clusters """
def initialize_cluster(sample):
    center = np.array(sample, dtype=float)
    covariance = np.identity(len(sample))  # # Covariância inicial - matriz identidade
    Lambda = 1  # Valor inicial de Lambda
    theta = initial_theta  # Valor inicial de theta 
    return center, covariance, Lambda, theta 

""" Atualizar cluster """
def update_cluster(center, covariance, sample, mu, omega, Lambda_prev, theta, efficiency, y, m=2):
    sample = np.array(sample, dtype=float)
    d = sample - center
    Lambda_new = Lambda_prev + mu ** m
    center_new = center + (d/Lambda_new) * mu 
    covariance_new =  (Lambda_prev / Lambda_new)*(covariance +
                      np.outer(d, d.T) * (mu**m / Lambda_new)) 
    # Atualizar theta usando omega
    theta_new = theta + omega * (efficiency - y)
    return center_new, covariance_new, Lambda_new, theta_new


""" Verificar se amostra representa novidade """
def novelty(sample, center, covariance):
    sample = np.array(sample, dtype=float)
    d = sample - center 
    inv_cov = np.linalg.inv(covariance)
    nov = np.exp(-0.5 * np.dot(np.dot(d.T, inv_cov), d))
    return nov

""" Calcular valor de omega """
def calculate_omega(sample, centers, covariances):
    sample = np.array(sample, dtype=float)
    membership_values = []
    for center, covariance in zip(centers, covariances):
        d = sample - center
        inv_cov = np.linalg.inv(covariance)
        mu = np.exp(-0.5 * np.dot(np.dot(d.T, inv_cov), d))
        membership_values.append(mu)
    
    sum_membership = sum(membership_values)
    omegas = [mu / sum_membership for mu in membership_values]
    return omegas, membership_values

""" Função para calcular eficiência do módulo. E feature = TSS."""
def efficiency(sample_df1,sample_df2, feature = 'TSS'):
    eff = (sample_df1[feature] - sample_df2[feature]) / sample_df1[feature]  * 100
    return np.float64(eff)

""" Função para calcular a saída y """
def fuzzy_output(omegas, thetas):
    return sum(omega * theta for omega, theta in zip(omegas, thetas))

""" Função para executar processamento das amostras """
def process_sample(sample, efficiency):
    global clusters, centers, covariances, Lambdas, thetas, updated_clusters, y, omegas_value, mus_value, theta_history, cluster_dict, theta_evolving
    sample = np.array(sample, dtype=float)
    # Se o vetor clusters estiver vazio a 1ª amostra será o 1º cluster
    if len(clusters) == 0:
        center, covariance, Lambda, theta = initialize_cluster(sample)
        clusters.append([sample])
        centers.append(center)
        covariances.append(covariance)
        Lambdas.append(Lambda)
        thetas.append(theta) 
        updated_clusters.append(0)  # Primeiro cluster criado
    else:
        max_nov = 0
        max_index = -1
        
        # Calcular novidade para cada cluster 
        for i, (center, covariance, Lambda, theta) in enumerate(zip(centers, covariances, Lambdas, thetas)):
            # Calcula a novidade da amostra em relação aos clusters existentes
            nov = novelty(sample, center, covariance)
            # Condição para identificar maior novidade
            if nov > max_nov:
                max_nov = nov
                max_index = i 
        
        # Calcular omegas e mu
        omegas, mus = calculate_omega(sample, centers, covariances)
        omegas_value = omegas
        mus_value = mus
        
        # Calcular saída do sistema fuzzy
        y = fuzzy_output(omegas, thetas) 
        
        # Verificar se amostra pertence a algum cluster existente
        if max_nov > novelty_threshold:
            theta_prev = thetas[max_index] # valor para verificar atualização
            print('Theta prévio:', theta_prev)
            centers[max_index], covariances[max_index], Lambdas[max_index], thetas[max_index] = update_cluster(
                centers[max_index], covariances[max_index], sample, mus[max_index], omegas[max_index], Lambdas[max_index], thetas[max_index], efficiency, y)
            clusters[max_index].append(sample) 
            updated_clusters.append(max_index)  # Registra o índice do cluster que foi atualizado
            theta_atual = thetas[max_index] # valor para verificar atualização
            
            # Comparação para atualiação "para cima" do theta

            if theta_prev > theta_atual:
                thetas[max_index] = theta_prev
            else:
                thetas[max_index] = theta_atual
            theta_evolving.append(thetas[max_index])
            print('Theta atual:', thetas[max_index]) 
            grafico(cluster_dict, updated_clusters[-1], thetas[max_index])

        else:
            # Se amostra não pertence a um cluster, um novo será criado.
            center, covariance, Lambda, theta = initialize_cluster(sample)
            clusters.append([sample])
            centers.append(center)
            covariances.append(covariance) 
            Lambdas.append(Lambda)
            thetas.append(theta) 
            updated_clusters.append(len(clusters) - 1)  # Registra o índice do novo cluster.
            grafico(cluster_dict, updated_clusters[-1], thetas[max_index])


""" Função para juntar clusters semelhantes"""
def merge_clusters():
    global centers, covariances, Lambdas, thetas, clusters
    to_merge = []
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            if novelty(centers[i], centers[j], covariances[j]) > merge_threshold:
                to_merge.append((i, j))
    
    for (i, j) in to_merge:
        if j < len(centers):  # Garantir que o J é válido após o merge.
            centers[i] = (centers[i] + centers[j]) / 2
            covariances[i] = (covariances[i] + covariances[j]) / 2
            Lambdas[i] = (Lambdas[i] + Lambdas[j]) / 2
            thetas[i] = (thetas[i] + thetas[j]) / 2
            clusters[i].extend(clusters[j])
            del centers[j]
            del covariances[j]
            del Lambdas[j]
            del thetas[j]
            del clusters[j]
            if j in updated_clusters:
                updated_clusters.remove(j)
    


# Carregar datasets para testes 
df_p1 = pd.read_csv('C:/Users/User/Desktop/PROG_A/datasets/df_ponto1.csv')
df_p2 = pd.read_csv('C:/Users/User/Desktop/PROG_A/datasets/df_ponto2.csv')
        
# Criar dataset menor para testes
numero_de_linhas = 9600
data1, data2 = sample_dataset(df_p1, df_p2, numero_de_linhas)

cont_geral = 0

# Função para simular o recebimento de amostras em tempo real

def main():
    global y, cont_geral
    cont = 0
    while True:
        # Calcular eficiência do módulo
        sample_df1 = data1.iloc[cont]
        sample_df2 = data2.iloc[cont]
        eff = efficiency(sample_df1,sample_df2, feature = 'TSS')
        # Coleta amostra
        sample = data1.iloc[cont] 
        sample =  normalise(sample)
        # Condição par atualizar theta
        if y <= eff:
            y = eff 
        # Rodar a função
        process_sample(sample, eff) 
        print(f"Cluster atualizado: {updated_clusters[-1]}")
        merge_clusters()
        #print(y)
        time.sleep(0.01)
        cont += 1
        cont_geral += 1
        print(cont_geral) 

if __name__ == "__main__":
    main()
    




# =============================================================================
# # Programa para treinar normalizador
# df_p1_values = df_p1.values # Extrair valores de dataset
# scaler = scaler.fit(df_p1_values) # Ajustar aos dados
# # Salvar o normalizador
# joblib.dump(scaler, 'C:/Users/User/Desktop/MSM_fuzzy/scaler.joblib')
# # Carregar o normalizador
# scaler = joblib.load('C:/Users/User/Desktop/MSM_fuzzy/scaler.joblib')
# # Testar função para normalizar dados
# normalise(sample)
# =============================================================================



"""
# Plotando os valores
plt.figure(figsize=(10, 6))
 
# Plotar cada cluster com uma cor diferente
for cluster_num, thetas in cluster_dict.items():
    plt.scatter([cluster_num] * len(thetas), thetas, label=f'Cluster {cluster_num}')

plt.xlabel('Cluster')
plt.ylabel('Theta')
plt.title('Theta Values per Cluster')
plt.legend()
plt.grid(True)
plt.show()
"""


















