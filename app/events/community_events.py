# Extensions
from app.extensions.database import db


def register_community_events():
    """Register all community-related event handlers"""
    from app.models.community import Community, CommunitySubscriber, CommunityModerator, CommunityBan
    
    @db.event.listens_for(Community, 'after_insert')
    def increment_communities_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.user_id
        ).values(
            communities_count=user_stats_table.c.communities_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(Community, 'after_delete')
    def decrement_community_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.user_id
        ).values(
            communities_count=user_stats_table.c.communities_count - 1
        )

        connection.execute(update_query)

    @db.event.listens_for(Community, 'before_delete')
    def decrement_subscriptions_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        for subscriber in target.subscribers:
            update_query = user_stats_table.update().where(
                user_stats_table.c.user_id == subscriber.user_id
            ).values(
                subscriptions_count=user_stats_table.c.subscriptions_count - 1
            )
            connection.execute(update_query)

    @db.event.listens_for(Community, 'before_delete')
    def decrement_moderations_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        for moderator in target.moderators:
            update_query = user_stats_table.update().where(
                user_stats_table.c.user_id == moderator.user_id
            ).values(
                moderations_count=user_stats_table.c.moderations_count - 1
            )
            connection.execute(update_query)

    @db.event.listens_for(CommunitySubscriber, 'after_insert')
    def increment_subscribers_count_on_community_stats(mapper, connection, target):
        from app.models.community import CommunityStats

        community_stats_table = CommunityStats.__table__

        
        update_query = community_stats_table.update().where(
            community_stats_table.c.community_id == target.community_id
        ).values(
            subscribers_count=community_stats_table.c.subscribers_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunitySubscriber, 'after_delete')
    def decrement_subscribers_count_on_community_stats(mapper, connection, target):
        from app.models.community import CommunityStats

        community_stats_table = CommunityStats.__table__
        
        update_query = community_stats_table.update().where(
            community_stats_table.c.community_id == target.community_id
        ).values(
            subscribers_count=community_stats_table.c.subscribers_count - 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunitySubscriber, 'after_insert')
    def increment_subscriptions_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.user_id
        ).values(
            subscriptions_count=user_stats_table.c.subscriptions_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunitySubscriber, 'after_delete')
    def decrement_subscriptions_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats
        
        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.user_id
        ).values(
            subscriptions_count=user_stats_table.c.subscriptions_count - 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunityModerator, 'after_insert')
    def increment_moderators_count_on_community_stats(mapper, connection, target):
        from app.models.community import CommunityStats

        community_stats_table = CommunityStats.__table__

        update_query = community_stats_table.update().where(
            community_stats_table.c.community_id == target.community_id
        ).values(
            moderators_count=community_stats_table.c.moderators_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunityModerator, 'after_delete')
    def decrement_moderators_count_on_community_stats(mapper, connection, target):
        from app.models.community import CommunityStats

        community_stats_table = CommunityStats.__table__

        update_query = community_stats_table.update().where(
            community_stats_table.c.community_id == target.community_id
        ).values(
            moderators_count=community_stats_table.c.moderators_count - 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunityModerator, 'after_insert')
    def increment_moderations_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.user_id
        ).values(
            moderations_count=user_stats_table.c.moderations_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunityModerator, 'after_delete')
    def decrement_moderations_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats
        
        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.user_id
        ).values(
            moderations_count=user_stats_table.c.moderations_count - 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunityBan, 'after_insert')
    def increment_banned_users_count_on_community_stats(mapper, connection, target):
        from app.models.community import CommunityStats

        community_stats_table = CommunityStats.__table__

        update_query = community_stats_table.update().where(
            community_stats_table.c.community_id == target.community_id
        ).values(
            banned_count=community_stats_table.c.banned_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(CommunityBan, 'after_delete')
    def decrement_banned_users_count_on_community_stats(mapper, connection, target):
        from app.models.community import CommunityStats

        community_stats_table = CommunityStats.__table__

        update_query = community_stats_table.update().where(
            community_stats_table.c.community_id == target.community_id
        ).values(
            banned_count=community_stats_table.c.banned_count - 1
        )

        connection.execute(update_query)


# Register events when module is imported
register_community_events()