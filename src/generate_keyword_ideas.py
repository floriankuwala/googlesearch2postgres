#local virtualenv --> my_google_ads_env

#load libaries and modules

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import csv
import time

# Initialize the Google Ads client.

client = GoogleAdsClient.load_from_storage("resources/google-ads.yaml") # Make sure to provide the path to the 'google-ads.yaml' file

customer_id = '66789990' # Replace with your own customer ID.

# Mapping of Months

month_mapping = {
    'JANUARY': '01',
    'FEBRUARY': '02',
    'MARCH': '03',
    'APRIL': '04',
    'MAY': '05',
    'JUNE': '06',
    'JULY': '07',
    'AUGUST': '08',
    'SEPTEMBER': '09',
    'OCTOBER': '10',
    'NOVEMBER': '11',
    'DECEMBER': '12'
}

def map_locations_ids_to_resource_names(client, location_ids):
    return [
        client.get_service("GeoTargetConstantService").geo_target_constant_path(location_id)
        for location_id in location_ids
    ]

def read_seed_keywords(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]



def write_csv_header(output_file, fieldnames):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def write_to_csv(results, output_file):
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['Seed Keyword', 'Keyword', 'Average Monthly Searches', 'Competition', 
        'Competition Index', 'Month', 'Monthly Searches','Average CPC','Low Top Bid',
        'High Top Bid','Keyword Annotation','Brand Bool', 'Concept Name', 'Concept Group']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        results = []
        for row in results:
            writer.writerow(row)


def main(client, customer_id, location_ids, language_id, keyword_text, seed_keyword):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    keyword_competition_level_enum = client.enums.KeywordPlanCompetitionLevelEnum
    keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
    keyword_annotation = client.enums.KeywordPlanKeywordAnnotationEnum

    
    location_rns = map_locations_ids_to_resource_names(client, location_ids)
    language_rn = client.get_service("GoogleAdsService").language_constant_path(language_id)
    
    request = client.get_type("GenerateKeywordIdeasRequest")  
    request.customer_id = customer_id
    request.language = language_rn
    request.geo_target_constants = location_rns
    request.include_adult_keywords = False
    request.keyword_plan_network = keyword_plan_network
    request.keyword_annotation = keyword_annotation

    request.keyword_seed.keywords.append(keyword_text)  

    with open('data/keyword_ideas.csv', 'a', newline='') as csvfile:
        fieldnames = ['seed_keyword','keyword', 'avg_monthly_searches', 'competition', 'competition_index', 
        'month', 'monthly_searches','cpc','low_range_bid','high_range_bid','keyword_annotation',
        'brand_bool','concept_group','concept_name','language_id', 'location_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        results = []

        try:
            keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(request=request)

            for idea in keyword_ideas.results:
                keyword_text = idea.text
                monthly_search_volume = idea.keyword_idea_metrics.avg_monthly_searches
                competition_value = idea.keyword_idea_metrics.competition.name
                competition_index = idea.keyword_idea_metrics.competition_index
                avg_cpc = idea.keyword_idea_metrics.average_cpc_micros / 1e6
                low_top_of_bid = idea.keyword_idea_metrics.low_top_of_page_bid_micros / 1e6 
                high_top_of_bid = idea.keyword_idea_metrics.high_top_of_page_bid_micros /1e6
                keyword_annotation = idea.keyword_annotations.concepts
                concept_name = "Unknown"
                concept_group_name = "Unknown"
            
                if keyword_annotation:
                 for concept in keyword_annotation:
                    if concept.name:
                        concept_name = concept.name
                    if concept.concept_group.name:
                        concept_group_name = concept.concept_group.name
            

                # Extract the 'type_' value from keyword_annotation
                brand_bool_value = "Unknown"  # Default value
                if keyword_annotation:
                    for concept in keyword_annotation:
                        if concept.concept_group.type_:
                            brand_bool_value = concept.concept_group.type_.name  # Assuming type_ has a 'name' attribute


                print(
                    f'Keyword idea text "{keyword_text}" has '
                    f'{monthly_search_volume} average monthly searches and '
                    f'"{competition_value}" competition.'
                    f'"{competition_index}" competition index.'
                    f'"{avg_cpc}" Average CPC.'
                    f'"{low_top_of_bid}" Low Top Bid.'
                    f'"{high_top_of_bid}" High Top Bid.'
                    f'"{keyword_annotation}" Keyword Annotation.'
                    f'"{brand_bool_value}" Brand Bool.'
                )

                for month in idea.keyword_idea_metrics.monthly_search_volumes:
                    month_name = month.month.name
                    month_number = month_mapping.get(month_name, '00')
                    formatted_date = f"{month.year}-{month_number}"
                    
                    print(
                        f"\tApproximately {month.monthly_searches} searches in "
                        f"{month.month.name}, {month.year}"
                    )
                    writer.writerow({
                        'seed_keyword': seed_keyword,
                        'keyword': keyword_text,
                        'avg_monthly_searches': monthly_search_volume,
                        'competition': competition_value,
                        'competition_index': competition_index,
                        'month': formatted_date,
                        'monthly_searches': month.monthly_searches,
                        'cpc': avg_cpc,
                        'low_range_bid': low_top_of_bid,
                        'high_range_bid': high_top_of_bid,
                        'keyword_annotation': keyword_annotation,
                        'brand_bool': brand_bool_value,
                        'concept_name': concept_name,
                        'concept_group': concept_group_name,
                        'language_id': language_id,
                        'location_id': location_ids[0]
                    })
                print("\n")

        except GoogleAdsException as ex:
            print(f"An error with code {ex.error.code().name} occurred: {ex.failure}")
        return results


def run():
    location_ids = ['2276']  
    language_id = '1001'  
    seed_keywords = read_seed_keywords('data/seed_keywords.txt')
    all_results = []

    fieldnames = ['seed_keyword','keyword', 'avg_monthly_searches', 'competition', 'competition_index', 'month', 'monthly_searches','cpc','low_range_bid','high_range_bid','keyword_annotation','brand_bool','concept_group','concept_name','language_id','location_id']
    write_csv_header('data/keyword_ideas.csv', fieldnames)
    
    for name in seed_keywords:
        result = main(client, customer_id, location_ids, language_id, name, name)
        if result:
            all_results.extend(result)
        time.sleep(1)  
    
    write_to_csv(all_results, 'data/keyword_ideas.csv')