class mmo_opt():
    # f - funkcja do optymalizacji
    # D - wymiar problemu
    # b_min, b_max - ograniczenia dolne i górne obszaru przeszukiwań
    # N - wielkość populacji
    # S - wielkość "drużyny"
    # mu, delta - parametry generatora losowości o rozkładzie normalnym
    # t_max - liczba iteracji
    def constructor(f, D, b_min, b_max, N, S, mu, delta, t_max):
        # dodatkowy wymiar słuzy do przechowywania wartości funkcji f
        player_base_current = array[N][D+1]
        player_base_best = array[N][D+1]
        
        # wypełnienie macierzy losowymi wartościami z przedziału (b_min, b_max)
        player_base_current.random(b_min, b_max)

        for player in player_base_current:
            # wstawienie do ostatniej komórki wiersza wartości funkcji wyliczonej na
            # podstawie wartości w pozostałych komórkach
            player[-1] = f(player[:-1])

        # macierz najlepszych rozwiązań dla każdego gracza jest w pierwszej iteracji
        # jest kopią aktualnych położeń każdej cząstki
        player_base_best = copy(player_base_current) 

        # znalezienie najlepszego dotychczas rozwiązania
        best_found = find_best_player(player_base_current)

    def run():
        for t in range(t_max):
            sort()
            move_players()
            update_values()
            find_best()

    def sort():
        # połączenie macierzy położeń i wartości aktualnych i najlepszych w jedną macierz
        # o wymiarach array[N][2D+2] po to by po sortowaniu nie utracić informacji o tym
        # które wiersze odnoszą się do tego saqmego gracza
        concat = concatenate((player_base_current, player_base_best))
        
        # sortowanie wierszy macierzy według kolumny o indeksie D
        concat = sort(concat, D)

        (player_base_current, player_base_best) = split(concat)

    def update_values():
        for player_base_current:
            player[-1] = f(player[:-1])

        for player_index in range(N):
            if player_base_current[player_index][-1] < player_base_best[player_index][-1]:
                player_base_best[player_index] = player_base_current[player_index]

    def find_best():
        best_found = find_best_player(player_base_best)

    def move_players():
        # ruch graczy należących do grupy I i III
        for player_index in range(N):
            if belongs_to_group_I(player_index):
                group_I_move(player_index)
            if belongs_to_group_III(player_index):
                group_III_move(player_index)
        
        # wybranie drużyn z graczy grupy II
        teams = matchmaking()

        # ruch graczy należących do grupy II
        for team in teams:
            group_II_move(team)
            
    def move_by_vector(index, vector):
        mod = array[D]
        # wpisanie do każdej komórki wektora modyfikacji zmienną losową o rozkładzie normalnym
        mod.random_normal(mu, delta)

        for dimension in range(D):
            vector[dimension] = vector[dimension]* mod[dimension]
        
        for dimension in range(D):
            player_base_current[index][dimension] = player_base_current[index][dimension] + vector[dimension]

    def group_I_move(index):
        # vector przechowuje dane o różnicy między najlepszym dotychczas znalezionym
        # rozwiązaniem, a aktualnym
        vector = array[D]
        for dimension in range(D):
            vector[dimension] = player_base_best[index][dimension] - player_base_current[index][dimension]
        
        move_by_vector(index, vector)

    def group_III_move(index):
        vector = array[D]
        for dimension in range(D):
            vector[dimension] = player_base_current[0][dimension] - player_base_current[index][dimension]
        
        move_by_vector(index, vector)

    def matchmaking()
        teams = list()
        team = list()
        # pobranie identyfikatory lig znajdujących się w grupie II
        leagues = get_leagues_of_group_II()

        for league in leagues:
            # zwraca listę indeksów w macierzy, które odnoszą się do graczy z danej ligi
            player_indices = get_player_indices_of_league()
            while True:
                # zwraca losowy element z listy; zwraca Null jeżeli lista jest pusta
                player_index = get_random_element(player_indices)
                if player_index is not Null:
                    team.append(player_index)
                    if length(team) == S:
                        teams.append(team)
                        team = list()
                    player_indices.delete_element(player_index)
                else:
                    break
        return teams

        
    def group_II_move(team):
        # znalezienie najlepszego gracza drużyny
        best_in_team = find_best_player_by_indices(team)
        for player_index in team:
            vector = array[D]
            for dimension in range(D):
                vector[dimension] = player_base_current[best_in_team][dimension] - player_base_current[player_index][dimension]
        
            move_by_vector(player_index, vector)


