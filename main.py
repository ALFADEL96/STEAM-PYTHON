import requests
import logging
import pandas as pd

# Preprocessing script authored by Abdulaziz Alfadel

# Configure logging
logging.basicConfig(filename='steam_reviews_errors.log', level=logging.ERROR)

def fetch_steam_reviews(app_id, max_reviews=100, language='english'):
    reviews = []
    params = {
        'json': 1,
        'filter': 'all',
        'language': language,
        'day_range': 9223372036854775807,
        'review_type': 'all',
        'purchase_type': 'all',
        'num_per_page': 100,  # Max allowed by API
        'cursor': '*'  # Starting cursor
    }

    while len(reviews) < max_reviews:
        url = f"https://store.steampowered.com/appreviews/{app_id}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            batch_reviews = data.get('reviews', [])
            reviews.extend(batch_reviews)
            # Check if we reached the end or collected enough reviews
            if not batch_reviews or len(reviews) >= max_reviews:
                break
            # Update cursor for next batch
            params['cursor'] = data.get('cursor', '*')
        else:
            error_message = f"Error fetching data for AppID {app_id}: Status Code {response.status_code}, Response: {response.text}"
            print(error_message)
            logging.error(error_message)
            break

    return reviews[:max_reviews]

def process_reviews(reviews):
    # Convert review data into a DataFrame
    df = pd.DataFrame(reviews)
    # Select relevant columns (customize this as needed)
    df = df[['recommendationid', 'author', 'language', 'review', 'timestamp_created', 'voted_up', 'votes_up', 'votes_funny', 'weighted_vote_score', 'comment_count']]
    return df

def save_reviews_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Saved reviews to {filename}")

# Main execution
if __name__ == "__main__":
    app_id = 1282100  # Example: Remnant 2
    num_reviews_to_fetch = 200  # Example: Fetch 200 reviews
    remnant_2_reviews = fetch_steam_reviews(app_id, max_reviews=num_reviews_to_fetch)

    if remnant_2_reviews:
        print(f"Reviews Fetched Successfully: {len(remnant_2_reviews)} reviews")
        # Process the reviews
        df_reviews = process_reviews(remnant_2_reviews)
        # Save to CSV
        save_reviews_to_csv(df_reviews, 'remnant_2_reviews.csv')
    else:
        print("Failed to fetch reviews.")
