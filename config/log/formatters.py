import logging

import sqlparse
import pygments
from pygments.lexers import SqlLexer
from pygments.formatters import Terminal256Formatter


class SQLFormatter(logging.Formatter):
    def format(self, record):

        sql = record.sql.strip()

        if sqlparse:
            # Indent the SQL query
            sql = sqlparse.format(sql, reindent=True)

        if pygments:
            # Highlight the SQL query
            sql = pygments.highlight(
                sql,
                SqlLexer(),
                Terminal256Formatter(style='monokai')
            )

        record.statement = sql
        return super(SQLFormatter, self).format(record)