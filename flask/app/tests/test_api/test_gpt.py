import json
import json

def test_begin_game(client, headers):
    json_data = {
        "game_environment": "test"
    }
    response = client.post("/gpt/begin_game", data=json.dumps(json_data),content_type='application/json', headers=headers)

    assert response.status_code == 200

def test_remove_game(client, headers):
    json_data = {
        "game_environment": "test"
    }
    response = client.post("/gpt/begin_game", data=json.dumps(json_data), content_type='application/json', headers=headers)
    assert response.status_code == 200
    game_id = response.json["id"]

    response = client.delete(f"/gpt/remove_game/{game_id}", headers=headers)
    assert response.status_code == 200

    response = client.get(f"/gpt/get_game/{game_id}", headers=headers)
    assert response.status_code == 404
