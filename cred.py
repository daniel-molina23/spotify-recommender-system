client_id='25719b244a394b4aac3b3c01bbe2bcdf'
client_secret='3273075dc4434a54a0567e056623d0d6'
# redirect_url = 'http://localhost:22/callback/'   # denied
# redirect_url = 'http://localhost:111/callback/'  # denied
# redirect_url = 'http://localhost:1715/callback/' # in use
# redirect_url = 'http://localhost:1720/callback/' # in use
# redirect_url = 'http://localhost:2049/callback/' # in use
# redirect_url = 'http://localhost:4949//callback' # in use
# redirect_url = 'http://localhost:7002/callback/' # in use
# redirect_url = "http://localhost:8000/callback/" # breaks
# redirect_url = "http://localhost:8888/callback/" # breaks
# redirect_url = "http://localhost:9000/callback/" # breaks
redirect_url = "https://example.com/callback/" # prompt
# redirect_url = "http://localhost/"


# from mpi4py import MPI
#
# comm = MPI.COMM_WORLD
# size = comm.Get_size()
# rank = comm.Get_rank()

# client_id = '25719b244a394b4aac3b3c01bbe2bcdf'
# client_secret = '9cdffadbb24040e5a7fd57810d47aa22'
# # redirect_url = 'https://localhost:9000/callback/'
#
# redirect_url = ""
# for i in range(size):
#     if rank == 0:
#         redirect_url = 'http://localhost:22/callback/'
#         break
#     elif rank == 1:
#         redirect_url = 'http://localhost:111/callback/'
#         break
#     elif rank == 2:
#         redirect_url = 'http://localhost:1715/callback/'
#         break
#     elif rank == 3:
#         redirect_url = 'http://localhost:1720/callback/'
#         break
#     elif rank == 4:
#         redirect_url = 'http://localhost:2049/callback/'
#         break
#     elif rank == 5:
#         redirect_url = 'http://localhost:4949//callback'
#         break
#     elif rank == 6:
#         redirect_url = 'http://localhost:7002/callback/'
#         break
#     elif rank == 7:
#         redirect_url = "http://localhost:8000/callback/"
#         break
#     elif rank == 8:
#         redirect_url = "http://localhost:8888/callback/"
#         break
#     elif rank == 9:
#         redirect_url = "http://localhost:9000/callback/"
#         break
#     elif rank == 10:
#         redirect_url = "https://example.com/callback/"
#         break
# print(rank, ":", redirect_url)