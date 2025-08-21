# Extensions
from app.extensions.database import db


def register_user_events():
    """Register all user-related event handlers"""
    from app.models.user import Follow
    
    @db.event.listens_for(Follow, 'after_insert')
    def increment_following_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.follower_id
        ).values(
            following_count=user_stats_table.c.following_count + 1
        )

        connection.execute(update_query)

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.followed_id
        ).values(
            followers_count=user_stats_table.c.followers_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(Follow, 'after_delete')
    def decrement_following_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.follower_id
        ).values(
            following_count=user_stats_table.c.following_count - 1
        )

        connection.execute(update_query)

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.followed_id
        ).values(
            followers_count=user_stats_table.c.followers_count - 1
        )

        connection.execute(update_query)


