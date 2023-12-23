import json

def test_begin_game(client, headers):
    json_data = {
        "game_environment": "test"
    }
    response = client.post("/gpt/begin_game", data=json.dumps(json_data),content_type='application/json', headers=headers)

    assert response.status_code == 200