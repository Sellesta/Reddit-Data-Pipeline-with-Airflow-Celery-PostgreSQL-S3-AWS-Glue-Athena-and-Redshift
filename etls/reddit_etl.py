import pandas as pd
import numpy as np
from praw import Reddit
import sys

from utils.constants import POST_FIELDS

def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
    
    try:
        
        reddit = Reddit(client_id = client_id,
                             client_secret = client_secret,
                             user_agent = user_agent)
        
        print("connected to Reddit")
        return reddit
    
    except Exception as e:
        print(e,"Connection error!!! Please check the access token keys")
        sys.exit(1)
        
def extract_post(reddit_instance : Reddit, subreddit: str, time_filter: str, limit= None):
    
    subreddit = reddit_instance.subreddit(subreddit)
    posts = subreddit.top(time_filter=time_filter, limit=limit)
    
    post_list = []
    
    # print(posts)
    
    for post in posts:
        post_dict = vars(post)
        # print(post_dict)
        
        post = {key: post_dict[key] for key in POST_FIELDS}
        
        post_list.append(post)
    return post_list

def transform_data(post_df: pd.DataFrame):
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    post_df['over_18'] = np.where((post_df['over_18'] == True), True, False)
    post_df['author'] = post_df['author'].astype(str)
    edited_mode = post_df['edited'].mode()
    post_df['edited'] = np.where(post_df['edited'].isin([True, False]),
                                 post_df['edited'], edited_mode).astype(bool)
    post_df['num_comments'] = post_df['num_comments'].astype(int)
    post_df['score'] = post_df['score'].astype(int)
    post_df['upvote_ratio'] = post_df['upvote_ratio'].astype(int)
    post_df['selftext'] = post_df['selftext'].astype(str)
    post_df['title'] = post_df['title'].astype(str)
    
    return post_df

def load_data_to_csv(data: pd.DataFrame, path:str):
    data.to_csv(path, index=False)
        
        
# [2024-01-24, 00:11:04 UTC] {logging_mixin.py:151} INFO - {'comment_limit': 2048, 'comment_sort': 'confidence', '_reddit': <praw.reddit.Reddit object at 0xffff79a1beb0>, 'approved_at_utc': None, 'subreddit': Subreddit(display_name='dataengineering'), 'selftext': 'For some reason, everytime I try to learn I see new tools and how they ease the existing work. And I end up wasting more time where if I spent that on actually learning, I would be way ahead. How do you know which tool to pick and choose(from the noise in the market) ?\n\nhttps://preview.redd.it/ji5thy5f05ec1.png?width=2013&format=png&auto=webp&s=167f4e2afce621cc135d5a0ff7d5c484fedaa032', 'author_fullname': 't2_rr6r6b8v', 'saved': False, 'mod_reason_title': None, 'gilded': 0, 'clicked': False, 'title': 'Is the Data Space really this Complicated or am I just overthinking?', 'link_flair_richtext': [], 'subreddit_name_prefixed': 'r/dataengineering', 'hidden': False, 'pwls': 6, 'link_flair_css_class': '', 'downs': 0, 'thumbnail_height': 72, 'top_awarded_type': None, 'hide_score': False, 'media_metadata': {'ji5thy5f05ec1': {'status': 'valid', 'e': 'Image', 'm': 'image/png', 'p': [{'y': 55, 'x': 108, 'u': 'https://preview.redd.it/ji5thy5f05ec1.png?width=108&crop=smart&auto=webp&s=407ea76e6c58768be8a3c4ec83b1e1c94a7f1ccd'}, {'y': 111, 'x': 216, 'u': 'https://preview.redd.it/ji5thy5f05ec1.png?width=216&crop=smart&auto=webp&s=c9fc662ada79e21acb1a19ca2d720fa384fa5b80'}, {'y': 165, 'x': 320, 'u': 'https://preview.redd.it/ji5thy5f05ec1.png?width=320&crop=smart&auto=webp&s=aa8a34aed3f57410d9ec1e07e19d12870b4eaaa6'}, {'y': 330, 'x': 640, 'u': 'https://preview.redd.it/ji5thy5f05ec1.png?width=640&crop=smart&auto=webp&s=0a5a2c5452da28f4a51f554df8ace1370adf7bb6'}, {'y': 496, 'x': 960, 'u': 'https://preview.redd.it/ji5thy5f05ec1.png?width=960&crop=smart&auto=webp&s=79d4e991f16ad3e962f34f36b200936b6c240e63'}, {'y': 558, 'x': 1080, 'u': 'https://preview.redd.it/ji5thy5f05ec1.png?width=1080&crop=smart&auto=webp&s=007ab4b69e95d325e31ea4357d1e22ee0f4a7d60'}], 's': {'y': 1041, 'x': 2013, 'u': 'https://preview.redd.it/ji5thy5f05ec1.png?width=2013&format=png&auto=webp&s=167f4e2afce621cc135d5a0ff7d5c484fedaa032'}, 'id': 'ji5thy5f05ec1'}}, 'name': 't3_19difxp', 'quarantine': False, 'link_flair_text_color': 'light', 'upvote_ratio': 0.89, 'author_flair_background_color': None, 'subreddit_type': 'public', 'ups': 71, 'total_awards_received': 0, 'media_embed': {}, 'thumbnail_width': 140, 'author_flair_template_id': None, 'is_original_content': False, 'user_reports': [], 'secure_media': None, 'is_reddit_media_domain': False, 'is_meta': False, 'category': None, 'secure_media_embed': {}, 'link_flair_text': 'Career', 'can_mod_post': False, 'score': 71, 'approved_by': None, 'is_created_from_ads_ui': False, 'author_premium': False, 'thumbnail': 'https://b.thumbs.redditmedia.com/NL2dUEcAl7BNg-wBWQxQmSI85U9S7otuZLi8-pjwXbA.jpg', 'edited': False, 'author_flair_css_class': None, 'author_flair_richtext': [], 'gildings': {}, 'content_categories': None, 'is_self': True, 'mod_note': None, 'created': 1705992902.0, 'link_flair_type': 'text', 'wls': 6, 'removed_by_category': None, 'banned_by': None, 'author_flair_type': 'text', 'domain': 'self.dataengineering', 'allow_live_comments': False, 'selftext_html': '<!-- SC_OFF --><div class="md"><p>For some reason, everytime I try to learn I see new tools and how they ease the existing work. And I end up wasting more time where if I spent that on actually learning, I would be way ahead. How do you know which tool to pick and choose(from the noise in the market) ?</p>\n\n<p><a href="https://preview.redd.it/ji5thy5f05ec1.png?width=2013&amp;format=png&amp;auto=webp&amp;s=167f4e2afce621cc135d5a0ff7d5c484fedaa032">https://preview.redd.it/ji5thy5f05ec1.png?width=2013&amp;format=png&amp;auto=webp&amp;s=167f4e2afce621cc135d5a0ff7d5c484fedaa032</a></p>\n</div><!-- SC_ON -->', 'likes': None, 'suggested_sort': None, 'banned_at_utc': None, 'view_count': None, 'archived': False, 'no_follow': False, 'is_crosspostable': False, 'pinned': False, 'over_18': False, 'all_awardings': [], 'awarders': [], 'media_only': False, 'link_flair_template_id': '069dd614-a7dc-11eb-8e48-0e90f49436a3', 'can_gild': False, 'spoiler': False, 'locked': False, 'author_flair_text': None, 'treatment_tags': [], 'visited': False, 'removed_by': None, 'num_reports': None, 'distinguished': None, 'subreddit_id': 't5_36en4', 'author_is_blocked': False, 'mod_reason_by': None, 'removal_reason': None, 'link_flair_background_color': '#349e48', 'id': '19difxp', 'is_robot_indexable': True, 'report_reasons': None, 'author': Redditor(name='_areebpasha'), 'discussion_type': None, 'num_comments': 72, 'send_replies': True, 'whitelist_status': 'all_ads', 'contest_mode': False, 'mod_reports': [], 'author_patreon_flair': False, 'author_flair_text_color': None, 'permalink': '/r/dataengineering/comments/19difxp/is_the_data_space_really_this_complicated_or_am_i/', 'parent_whitelist_status': 'all_ads', 'stickied': False, 'url': 'https://www.reddit.com/r/dataengineering/comments/19difxp/is_the_data_space_really_this_complicated_or_am_i/', 'subreddit_subscribers': 155234, 'created_utc': 1705992902.0, 'num_crossposts': 0, 'media': None, 'is_video': False, '_fetched': False, '_additional_fetch_params': {}, '_comments_by_id': {}}

        
    