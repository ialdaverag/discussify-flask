# Extensions
from app.extensions.database import db


def register_post_events():
    """Register all post-related event handlers"""
    from app.models.post import Post, PostVote, PostBookmark
    
    @db.event.listens_for(Post, 'after_insert')
    def increment_posts_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.user_id
        ).values(
            posts_count=user_stats_table.c.posts_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(Post, 'after_delete')
    def decrement_posts_count_on_user_stats(mapper, connection, target):
        from app.models.user import UserStats

        user_stats_table = UserStats.__table__

        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == target.user_id
        ).values(
            posts_count=user_stats_table.c.posts_count - 1
        )

        connection.execute(update_query)

    @db.event.listens_for(Post, 'after_insert')
    def increment_posts_count_on_community_stats(mapper, connection, target):
        from app.models.community import CommunityStats

        community_stats_table = CommunityStats.__table__

        update_query = community_stats_table.update().where(
            community_stats_table.c.community_id == target.community_id
        ).values(
            posts_count=community_stats_table.c.posts_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(Post, 'after_delete')
    def decrement_posts_count_on_community_stats(mapper, connection, target):
        from app.models.community import CommunityStats

        community_stats_table = CommunityStats.__table__

        update_query = community_stats_table.update().where(
            community_stats_table.c.community_id == target.community_id
        ).values(
            posts_count=community_stats_table.c.posts_count - 1
        )

        connection.execute(update_query)

    @db.event.listens_for(PostVote, 'after_insert')
    def increment_votes_count_on_post_stats(mapper, connection, target):
        from app.models.post import PostStats

        post_stats_table = PostStats.__table__

        if target.direction == 1:  # upvote
            update_query = post_stats_table.update().where(
                post_stats_table.c.post_id == target.post_id
            ).values(
                upvotes_count=post_stats_table.c.upvotes_count + 1
            )
        elif target.direction == -1:  # downvote
            update_query = post_stats_table.update().where(
                post_stats_table.c.post_id == target.post_id
            ).values(
                downvotes_count=post_stats_table.c.downvotes_count + 1
            )

        connection.execute(update_query)

    @db.event.listens_for(PostVote, 'after_delete')
    def decrement_votes_count_on_post_stats(mapper, connection, target):
        from app.models.post import PostStats

        post_stats_table = PostStats.__table__

        if target.direction == 1:  # upvote
            update_query = post_stats_table.update().where(
                post_stats_table.c.post_id == target.post_id
            ).values(
                upvotes_count=post_stats_table.c.upvotes_count - 1
            )
        elif target.direction == -1:  # downvote
            update_query = post_stats_table.update().where(
                post_stats_table.c.post_id == target.post_id
            ).values(
                downvotes_count=post_stats_table.c.downvotes_count - 1
            )

        connection.execute(update_query)

    @db.event.listens_for(PostVote.direction, 'set')
    def update_votes_count_on_post_stats(target, value, oldvalue, initiator):
        from app.models.post import PostStats

        post_stats_table = PostStats.__table__

        if oldvalue is not None and oldvalue != value:  # the vote direction has changed
            if value == 1:  # changed to upvote
                update_query = post_stats_table.update().where(
                    post_stats_table.c.post_id == target.post_id
                ).values(
                    upvotes_count=post_stats_table.c.upvotes_count + 1,
                    downvotes_count=post_stats_table.c.downvotes_count - 1
                )
            elif value == -1:  # changed to downvote
                update_query = post_stats_table.update().where(
                    post_stats_table.c.post_id == target.post_id
                ).values(
                    upvotes_count=post_stats_table.c.upvotes_count - 1,
                    downvotes_count=post_stats_table.c.downvotes_count + 1
                )

            db.session.execute(update_query)

    @db.event.listens_for(PostBookmark, 'after_insert')
    def increment_bookmarks_count_on_post_stats(mapper, connection, target):
        from app.models.post import PostStats

        post_stats_table = PostStats.__table__

        update_query = post_stats_table.update().where(
            post_stats_table.c.post_id == target.post_id
        ).values(
            bookmarks_count=post_stats_table.c.bookmarks_count + 1
        )

        connection.execute(update_query)

    @db.event.listens_for(PostBookmark, 'after_delete')
    def decrement_bookmarks_count_on_post_stats(mapper, connection, target):
        from app.models.post import PostStats

        post_stats_table = PostStats.__table__

        update_query = post_stats_table.update().where(
            post_stats_table.c.post_id == target.post_id
        ).values(
            bookmarks_count=post_stats_table.c.bookmarks_count - 1
        )

        connection.execute(update_query)


# Register events when module is imported
register_post_events()