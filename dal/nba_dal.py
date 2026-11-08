import os
from sqlalchemy import create_engine, MetaData, Table, text, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL

db = create_engine(os.environ['DB_URL'])
metadata = MetaData()
teams_table = Table('teams', metadata, autoload_with=db)
players_table = Table('players', metadata, autoload_with=db)
games_table = Table('games', metadata, autoload_with=db)
games_details_table = Table('games_details', metadata, autoload_with=db)


def search_players_by_team(team_abbreviation, season=None, limit=100):
    with db.connect() as connection:
        if season:
            result_set = connection.execute(text("""
                SELECT p.PLAYER_ID, p.PLAYER_NAME, p.TEAM_ID, p.SEASON, t.ABBREVIATION, t.NICKNAME
                FROM players p
                INNER JOIN teams t ON p.TEAM_ID = t.TEAM_ID
                WHERE t.ABBREVIATION = :team_abbr AND p.SEASON = :season
                ORDER BY p.PLAYER_NAME
                LIMIT :limit
            """), {"team_abbr": team_abbreviation, "season": season, "limit": limit})
        else:
            result_set = connection.execute(text("""
                SELECT p.PLAYER_ID, p.PLAYER_NAME, p.TEAM_ID, p.SEASON, t.ABBREVIATION, t.NICKNAME
                FROM players p
                INNER JOIN teams t ON p.TEAM_ID = t.TEAM_ID
                WHERE t.ABBREVIATION = :team_abbr
                ORDER BY p.SEASON DESC, p.PLAYER_NAME
                LIMIT :limit
            """), {"team_abbr": team_abbreviation, "limit": limit})
        result = result_set.fetchall()
        return list(result)


def get_player_average_stats(player_id, season=None):
    from sqlalchemy.sql import select
    with db.connect() as connection:
        if season:
            statement = select(
                func.avg(games_details_table.c.pts).label('avg_points'),
                func.avg(games_details_table.c.reb).label('avg_rebounds'),
                func.avg(games_details_table.c.ast).label('avg_assists'),
                func.avg(games_details_table.c.stl).label('avg_steals'),
                func.avg(games_details_table.c.blk).label('avg_blocks'),
                func.count(games_details_table.c.game_id).label('games_played')
            ).where(
                games_details_table.c.player_id == player_id
            ).join(
                games_table, games_details_table.c.game_id == games_table.c.game_id
            ).where(
                games_table.c.season == season
            )
        else:
            statement = select(
                func.avg(games_details_table.c.pts).label('avg_points'),
                func.avg(games_details_table.c.reb).label('avg_rebounds'),
                func.avg(games_details_table.c.ast).label('avg_assists'),
                func.avg(games_details_table.c.stl).label('avg_steals'),
                func.avg(games_details_table.c.blk).label('avg_blocks'),
                func.count(games_details_table.c.game_id).label('games_played')
            ).where(
                games_details_table.c.player_id == player_id
            )
        
        result_set = connection.execute(statement)
        result = result_set.fetchone()
        
        if result and result.games_played > 0:
            return {
                'avg_points': round(float(result.avg_points or 0), 2),
                'avg_rebounds': round(float(result.avg_rebounds or 0), 2),
                'avg_assists': round(float(result.avg_assists or 0), 2),
                'avg_steals': round(float(result.avg_steals or 0), 2),
                'avg_blocks': round(float(result.avg_blocks or 0), 2),
                'games_played': result.games_played
            }
        return None


ORM_Base = declarative_base()


class Team(ORM_Base):
    __tablename__ = 'teams'
    
    team_id = Column(Integer, primary_key=True)
    league_id = Column(Integer)
    min_year = Column(Integer)
    max_year = Column(Integer)
    abbreviation = Column(String(10))
    nickname = Column(String(50))
    yearfounded = Column(Integer)
    city = Column(String(50))
    arena = Column(String(100))
    arenacapacity = Column(Integer)
    owner = Column(String(100))
    generalmanager = Column(String(100))
    headcoach = Column(String(100))
    dleagueaffiliation = Column(String(100))


class Player(ORM_Base):
    __tablename__ = 'players'
    
    player_id = Column(Integer, primary_key=True)
    player_name = Column(String(100))
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    season = Column(Integer)
    
    team = relationship('Team', foreign_keys=[team_id])


class Game(ORM_Base):
    __tablename__ = 'games'
    
    game_id = Column(Integer, primary_key=True)
    game_date_est = Column(Date)
    game_status_text = Column(String(50))
    home_team_id = Column(Integer, ForeignKey('teams.team_id'))
    visitor_team_id = Column(Integer, ForeignKey('teams.team_id'))
    season = Column(Integer)
    team_id_home = Column(Integer)
    pts_home = Column(Integer)
    fg_pct_home = Column(DECIMAL(5,3))
    ft_pct_home = Column(DECIMAL(5,3))
    fg3_pct_home = Column(DECIMAL(5,3))
    ast_home = Column(Integer)
    reb_home = Column(Integer)
    team_id_away = Column(Integer)
    pts_away = Column(Integer)
    fg_pct_away = Column(DECIMAL(5,3))
    ft_pct_away = Column(DECIMAL(5,3))
    fg3_pct_away = Column(DECIMAL(5,3))
    ast_away = Column(Integer)
    reb_away = Column(Integer)
    home_team_wins = Column(Integer)
    
    home_team = relationship('Team', foreign_keys=[home_team_id])
    visitor_team = relationship('Team', foreign_keys=[visitor_team_id])
    

class GameDetail(ORM_Base):
    __tablename__ = 'games_details'
    
    game_id = Column(Integer, ForeignKey('games.game_id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    player_id = Column(Integer, ForeignKey('players.player_id'), primary_key=True)
    team_abbreviation = Column(String(10))
    team_city = Column(String(50))
    player_name = Column(String(100))
    nickname = Column(String(50))
    start_position = Column(String(10))
    comment = Column(String(200))
    min = Column(String(10))
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(DECIMAL(5,3))
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(DECIMAL(5,3))
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(DECIMAL(5,3))
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    to = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Integer)
    
    game = relationship('Game', foreign_keys=[game_id])
    team = relationship('Team', foreign_keys=[team_id])
    player = relationship('Player', foreign_keys=[player_id])


Session = sessionmaker(bind=db)


def get_team_season_record(team_abbreviation, season):
    session = Session()
    try:
        query = session.query(Game).\
            join(Team, Game.home_team_id == Team.team_id).\
            filter(Team.abbreviation == team_abbreviation).\
            filter(Game.season == season)
        
        home_games = query.all()
        
        query_away = session.query(Game).\
            join(Team, Game.visitor_team_id == Team.team_id).\
            filter(Team.abbreviation == team_abbreviation).\
            filter(Game.season == season)
        
        away_games = query_away.all()
        
        total_games = len(home_games) + len(away_games)
        wins = 0
        
        for game in home_games:
            if game.home_team_wins == 1:
                wins += 1
        
        for game in away_games:
            if game.home_team_wins == 0:
                wins += 1
        
        losses = total_games - wins
        win_percentage = round(wins / total_games * 100, 2) if total_games > 0 else 0
        
        return {
            'team': team_abbreviation,
            'season': season,
            'wins': wins,
            'losses': losses,
            'total_games': total_games,
            'win_percentage': win_percentage
        }
    finally:
        session.close()

# CRUD: CREATE - Add Player to Team

def add_player_to_team(player_name, team_abbreviation, season):
    session = Session()
    try:
        team = session.query(Team).filter(Team.abbreviation == team_abbreviation).first()
        
        if not team:
            return None
        
        max_id = session.query(func.max(Player.player_id)).scalar()
        next_id = (max_id or 0) + 1
        
        player = Player(
            player_id=next_id,
            player_name=player_name,
            team_id=team.team_id,
            season=season
        )
        
        session.add(player)
        session.commit()
        
        session.refresh(player)
        _ = player.team  
        
        session.expunge(player)
        
        return player
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# CRUD: READ - Search Players by Name

def search_players_by_name(player_name, limit=20):
    with db.connect() as connection:
        result_set = connection.execute(text("""
            SELECT p.PLAYER_ID, p.PLAYER_NAME, t.ABBREVIATION, p.SEASON
            FROM players p
            INNER JOIN teams t ON p.TEAM_ID = t.TEAM_ID
            WHERE LOWER(p.PLAYER_NAME) LIKE LOWER(:search_term)
            ORDER BY p.SEASON DESC, p.PLAYER_NAME
            LIMIT :limit
        """), {"search_term": f"%{player_name}%", "limit": limit})
        return list(result_set.fetchall())
    
# CRUD: READ - Get Player by ID

def get_player_by_id(player_id):
    session = Session()
    try:
        player = session.query(Player).filter(Player.player_id == player_id).first()
        if player:
            _ = player.team  
            session.expunge(player)  
        return player
    finally:
        session.close()
        
# CRUD: UPDATE - Update Player's Information

def update_player(player_id, team_abbreviation=None, season=None, player_name=None):
    session = Session()
    try:
        player = session.query(Player).filter(Player.player_id == player_id).first()
        
        if not player:
            return None
        
        if team_abbreviation:
            team = session.query(Team).filter(Team.abbreviation == team_abbreviation).first()
            if not team:
                return None
            player.team_id = team.team_id
            
        if season is not None:
            player.season = season
            
        if player_name:
            player.player_name = player_name
            
        session.commit()
        session.refresh(player)
        _ = player.team  
        session.expunge(player)  
        return player
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        
# CRUD: DELETE - DELETE PLAYER
        
def delete_player(player_id):
    session = Session()
    try:
        player = session.query(Player).filter(Player.player_id == player_id).first()
        
        if not player:
            return None
        
        player_name = player.player_name
        
        games_deleted = session.query(GameDetail).\
            filter(GameDetail.player_id == player_id).\
            delete(synchronize_session=False)
            
        session.delete(player)
        
        session.commit()
        
        return {
            'player_id': player_id,
            'player_name': player_name,
            'games_deleted': games_deleted,
            'player_deleted': True
        }
    
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()