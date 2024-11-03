import requests

from config import API_DOMAIN


class RequestHandler:
    def __init__(self):
        self.domain = API_DOMAIN

    def shorten_url(self, long_url: str):
        """Sends POST request to fastAPI endpoint path=/shorten/"""
        url = f"{self.domain}/shorten/?long_url={long_url}"

        try:
            response = requests.post(url)
            response.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")  # Log the error message
            if response is not None:
                print(f"Status Code: {response.status_code}")  # Print the status code
                print(
                    f"Response Content: {response.text}"
                )  # Print the raw response text
                try:
                    print(
                        f"Response JSON: {response.json()}"
                    )  # Attempt to print JSON response
                except ValueError:
                    print("Response is not in JSON format.")
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle other exceptions

        # If no exceptions were raised, the response is successful
        else:
            print("Request was successful!")
            return response.json()

    def fetch_long_url(self, short_url: str):
        """Sends GET request to fastAPI endpoint path=/fetch/{short_url}"""
        url = f"{self.domain}/fetch/{short_url}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")  # Log the error message
            if response is not None:
                print(f"Status Code: {response.status_code}")  # Print the status code
                print(
                    f"Response Content: {response.text}"
                )  # Print the raw response text
                try:
                    print(
                        f"Response JSON: {response.json()}"
                    )  # Attempt to print JSON response
                except ValueError:
                    print("Response is not in JSON format.")
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle other exceptions

        # If no exceptions were raised, the response is successful
        else:
            print("Request was successful!")
            return response.json()
