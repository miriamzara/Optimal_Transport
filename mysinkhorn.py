import numpy as np
import time

def funzione_costo(N, G, C):
    val = 0
    for i in range(N):
        for j in range(N):
            val += C[i][j] * G[i][j]
    return val


def sinkhorn_solver(m1, m2, epsilon, C):
    # INPUT MASS VECTORS
    N1 = len(m1)
    N2 = len(m2)
    if N1 != N2:
        print("ERROR: The two histograms have different dimensions!")
        exit(1)
    N = N1
    # NORMALIZE COST MATRIX
    C = C/np.max(C)
    # INITIALIZATION: definition of the kernel, definition of A, B
    K = np.zeros(N*N)
    A = np.zeros(N)
    B = np.ones(N)
    # Transport plan G
    G = np.zeros((N, N))
    # SINKHORN
    # Convergence criterion = relative change of the infinity norm of B < conv
    # Set a maximum number of iterations to avoid an infinite loop in case of non-convergence
    n_iterazioni_massime = 1000
    n_iterazioni_effettive = 0
    conv = 0.01  # allowed relative change = 1%
    # Initialization of the kernel
    K = np.exp(-C / epsilon)
    variazione = 1
    is_ended = 0
    norma_infty = 0
    norma_infty_bis = 1

    while variazione > conv and is_ended == 0:
        n_iterazioni_effettive += 1
        norma_infty = norma_infty_bis
        norma_infty_bis = np.finfo(float).min
        # Update A
        A = m1 / (K @ B)
        if np.any(np.isnan(A)):
            print(f"Algorithm exploded at iteration {n_iterazioni_effettive}")
            exit(1)
        # Update B
        B = m2 / (K.transpose() @ A)
        if np.any(np.isnan(B)):
            print(f"Algorithm exploded at iteration {n_iterazioni_effettive}")
            exit(1)
        norma_infty_bis = np.max(B)
        # Check convergence criterion
        variazione = (np.abs(norma_infty_bis - norma_infty) / norma_infty)
        # Stop safety
        if n_iterazioni_effettive > n_iterazioni_massime:
            is_ended = 1
            print(f"Maximum number of iterations reached ({n_iterazioni_massime}), convergence criterion NOT reached")
            break
    
        for k in range(N1):
            for l in range(N2):
                G[k][l] = A[k] * K[k][l] * B[l]
    return G