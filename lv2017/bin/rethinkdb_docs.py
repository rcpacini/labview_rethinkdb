def rethinkdb()
    '''r -> r
    
    The top-level ReQL namespace.
    
    *Example* Setup your top-level namespace.
    
        import rethinkdb as r
    
    '''
def rethinkdb.add()
    '''value + value -> value
    time + number -> time
    value.add(value[, value, ...]) -> value
    time.add(number[, number, ...]) -> time
    
    Sum two or more numbers, or concatenate two or more strings or arrays.
    
    The `add` command can be called in either prefix or infix form; both forms are equivalent. Note that ReQL will not perform type coercion. You cannot, for example, `add` a string and a number together.
    
    *Example* It\'s as easy as 2 + 2 = 4.
    
        > (r.expr(2) + 2).run(conn)
        
        4
    
    *Example* Concatenate strings.
    
        > (r.expr("foo") + "bar" + "baz").run(conn)
        
        "foobarbaz"
    
    *Example* Concatenate arrays.
    
        > (r.expr(["foo", "bar"]) + ["buzz"]).run(conn)
        
        ["foo", "bar", "buzz"]
    
    *Example* Create a date one year from now.
    
        (r.now() + 365*24*60*60).run(conn)
    
    *Example* Use [args](http://rethinkdb.com/api/python/args) with `add` to sum multiple values.
    
        > vals = [10, 20, 30]
        > r.add(r.args(vals)).run(conn)
        
        60
    
    *Example* Concatenate an array of strings with `args`.
    
        > vals = [\'foo\', \'bar\', \'buzz\']
        > r.add(r.args(vals)).run(conn)
        
        "foobarbuzz"
    '''
def rethinkdb.and_()
    '''bool & bool -> bool
    bool.and_([bool, bool, ...]) -> bool
    r.and_([bool, bool, ...]) -> bool
    
    Compute the logical "and" of one or more values.
    
    The `and_` command can be used as an infix operator after its first argument (`r.expr(True).and_(False)`) or given all of its arguments as parameters (`r.and_(True, False)`). The standard Python and operator, `&`, may also be used with ReQL.
    
    Calling `and_` with zero arguments will return `True`.
    
    *Example* Return whether both `a` and `b` evaluate to true.
    
        > a = True
        > b = False
        > (r.expr(a) & b).run(conn)
        
        False
    *Example* Return whether all of `x`, `y` and `z` evaluate to true.
    
        > x = True
        > y = True
        > z = True
        > r.and_(x, y, z).run(conn)
        
        True
    '''
def rethinkdb.args()
    '''r.args(array) -> special
    
    `r.args` is a special term that's used to splice an array of arguments
    into another term.  This is useful when you want to call a variadic
    term such as [get_all](http://rethinkdb.com/api/python/get_all/) with a set of arguments produced at runtime.
    
    This is analogous to unpacking argument lists in Python.
    
    *Example* Get Alice and Bob from the table `people`.
    
        r.table('people').get_all('Alice', 'Bob').run(conn)
        # or
        r.table('people').get_all(r.args(['Alice', 'Bob'])).run(conn)
    
    *Example* Get all of Alice's children from the table `people`.
    
        # r.table('people').get('Alice') returns {'id': 'Alice', 'children': ['Bob', 'Carol']}
        r.table('people').get_all(r.args(r.table('people').get('Alice')['children'])).run(conn)
    "'''
def rethinkdb.ast.DB.table()
    '''db.table(name[, read_mode='single', identifier_format='name']) -> table
    
    Return all documents in a table. Other commands may be chained after `table` to return a subset of documents (such as [get](http://rethinkdb.com/api/python/get/) and [filter](http://rethinkdb.com/api/python/filter/)) or perform further processing.
    
    *Example* Return all documents in the table 'marvel' of the default database.
    
        r.table('marvel').run(conn)
    
    *Example* Return all documents in the table 'marvel' of the database 'heroes'.
    
        r.db('heroes').table('marvel').run(conn)
    
    There are two optional arguments.
    
    * `read_mode`: One of three possible values affecting the consistency guarantee for the table read:
        * `single` returns values that are in memory (but not necessarily written to disk) on the primary replica. This is the default.
        * `majority` will only return values that are safely committed on disk on a majority of replicas. This requires sending a message to every replica on each read, so it is the slowest but most consistent.
        * `outdated` will return values that are in memory on an arbitrarily-selected replica. This is the fastest but least consistent.
    * `identifier_format`: possible values are `name` and `uuid`, with a default of `name`. If set to `uuid`, then [system tables](http://rethinkdb.com/docs/system-tables/) will refer to servers, databases and tables by UUID rather than name. (This only has an effect when used with system tables.)
    
    *Example* Allow potentially out-of-date data in exchange for faster reads.
    
        r.db('heroes').table('marvel', read_mode='outdated').run(conn)
    "'''
def rethinkdb.ast.DB.table_create()
    '''db.table_create(table_name[, options]) -> object
    r.table_create(table_name[, options]) -> object
    
    Create a table. A RethinkDB table is a collection of JSON documents.
    
    If successful, the command returns an object with two fields:
    
    * `tables_created`: always `1`.
    * `config_changes`: a list containing one two-field object, `old_val` and `new_val`:
        * `old_val`: always `None`.
        * `new_val`: the table\'s new [config](http://rethinkdb.com/api/python/config) value.
    
    If a table with the same name already exists, the command throws `ReqlOpFailedError`.
    
    When creating a table you can specify the following options:
    
    * `primary_key`: the name of the primary key. The default primary key is `id`.
    * `durability`: if set to `soft`, writes will be acknowledged by the server immediately and flushed to disk in the background. The default is `hard`: acknowledgment of writes happens after data has been written to disk.
    * `shards`: the number of shards, an integer from 1-64. Defaults to `1`.
    * `replicas`: either an integer or a mapping object. Defaults to `1`.
        * If `replicas` is an integer, it specifies the number of replicas per shard. Specifying more replicas than there are servers will return an error.
        * If `replicas` is an object, it specifies key-value pairs of server tags and the number of replicas to assign to those servers: `{\'tag1\': 2, \'tag2\': 4, \'tag3\': 2, ...}`.
    * `primary_replica_tag`: the primary server specified by its server tag. Required if `replicas` is an object; the tag must be in the object. This must *not* be specified if `replicas` is an integer.
    
    The data type](http://rethinkdb.com/docs/data-types/) of a primary key is usually a string (like a UUID) or a number, but it can also be a time, binary object, boolean or an array. Data types can be mixed in the primary key field, but all values must be unique. Using an array as a primary key creates a compound index; read the documentation on [compound secondary indexes for more information, as it applies to primary keys as well. Primary keys cannot be objects.
    
    Tables will be available for writing when the command returns.
    
    *Example* Create a table named \'dc_universe\' with the default settings.
    
        r.db(\'heroes\').table_create(\'dc_universe\').run(conn)
        
        {
            "config_changes": [
                {
                    "new_val": {
                        "db": "test",
                        "durability":  "hard",
                        "id": "20ea60d4-3b76-4817-8828-98a236df0297",
                        "name": "dc_universe",
                        "primary_key": "id",
                        "shards": [
                            {
                                "primary_replica": "rethinkdb_srv1",
                                "replicas": [
                                    "rethinkdb_srv1",
                                    "rethinkdb_srv2"
                                ]
                            }
                        ],
                        "write_acks": "majority"
                    },
                    "old_val": None
                }
            ],
            "tables_created": 1
        }
    
    *Example* Create a table named \'dc_universe\' using the field \'name\' as primary key.
    
        r.db(\'test\').table_create(\'dc_universe\', primary_key=\'name\').run(conn)
    
    *Example* Create a table set up for two shards and three replicas per shard. This requires three available servers.
    
        r.db(\'test\').table_create(\'dc_universe\', shards=2, replicas=3).run(conn)
    
    Read [Sharding and replication](http://rethinkdb.com/docs/sharding-and-replication/) for a complete discussion of the subject, including advanced topics.
    '''
def rethinkdb.ast.DB.table_drop()
    '''db.table_drop(table_name) -> object
    
    Drop a table. The table and all its data will be deleted.
    
    If successful, the command returns an object with two fields:
    
    * `tables_dropped`: always `1`.
    * `config_changes`: a list containing one two-field object, `old_val` and `new_val`:
        * `old_val`: the dropped table\'s [config](http://rethinkdb.com/api/python/config) value.
        * `new_val`: always `None`.
    
    If the given table does not exist in the database, the command throws `ReqlRuntimeError`.
    
    *Example* Drop a table named \'dc_universe\'.
    
        r.db(\'test\').table_drop(\'dc_universe\').run(conn)
        
        {
            "config_changes": [
                {
                    "old_val": {
                        "db": "test",
                        "durability":  "hard",
                        "id": "20ea60d4-3b76-4817-8828-98a236df0297",
                        "name": "dc_universe",
                        "primary_key": "id",
                        "shards": [
                            {
                                "primary_replica": "rethinkdb_srv1",
                                "replicas": [
                                    "rethinkdb_srv1",
                                    "rethinkdb_srv2"
                                ]
                            }
                        ],
                        "write_acks": "majority"
                    },
                    "new_val": None
                }
            ],
            "tables_dropped": 1
        }
    '''
def rethinkdb.ast.DB.table_list()
    '''db.table_list() -> array
    
    List all table names in a database. The result is a list of strings.
    
    *Example* List all tables of the 'test' database.
    
        r.db('test').table_list().run(conn)
        
    "'''
def rethinkdb.ast.RqlQuery.__add__()
    '''value + value -> value
    time + number -> time
    value.add(value[, value, ...]) -> value
    time.add(number[, number, ...]) -> time
    
    Sum two or more numbers, or concatenate two or more strings or arrays.
    
    The `add` command can be called in either prefix or infix form; both forms are equivalent. Note that ReQL will not perform type coercion. You cannot, for example, `add` a string and a number together.
    
    *Example* It\'s as easy as 2 + 2 = 4.
    
        > (r.expr(2) + 2).run(conn)
        
        4
    
    *Example* Concatenate strings.
    
        > (r.expr("foo") + "bar" + "baz").run(conn)
        
        "foobarbaz"
    
    *Example* Concatenate arrays.
    
        > (r.expr(["foo", "bar"]) + ["buzz"]).run(conn)
        
        ["foo", "bar", "buzz"]
    
    *Example* Create a date one year from now.
    
        (r.now() + 365*24*60*60).run(conn)
    
    *Example* Use [args](http://rethinkdb.com/api/python/args) with `add` to sum multiple values.
    
        > vals = [10, 20, 30]
        > r.add(r.args(vals)).run(conn)
        
        60
    
    *Example* Concatenate an array of strings with `args`.
    
        > vals = [\'foo\', \'bar\', \'buzz\']
        > r.add(r.args(vals)).run(conn)
        
        "foobarbuzz"
    '''
def rethinkdb.ast.RqlQuery.__and__()
    '''bool & bool -> bool
    bool.and_([bool, bool, ...]) -> bool
    r.and_([bool, bool, ...]) -> bool
    
    Compute the logical "and" of one or more values.
    
    The `and_` command can be used as an infix operator after its first argument (`r.expr(True).and_(False)`) or given all of its arguments as parameters (`r.and_(True, False)`). The standard Python and operator, `&`, may also be used with ReQL.
    
    Calling `and_` with zero arguments will return `True`.
    
    *Example* Return whether both `a` and `b` evaluate to true.
    
        > a = True
        > b = False
        > (r.expr(a) & b).run(conn)
        
        False
    *Example* Return whether all of `x`, `y` and `z` evaluate to true.
    
        > x = True
        > y = True
        > z = True
        > r.and_(x, y, z).run(conn)
        
        True
    '''
def rethinkdb.ast.RqlQuery.__div__()
    '''number / number -> number
    number.div(number[, number ...]) -> number
    
    Divide two numbers.
    
    *Example* It's as easy as 2 / 2 = 1.
    
        (r.expr(2) / 2).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.__eq__()
    '''value.eq(value[, value, ...]) -> bool
    value == value -> bool
    
    Test if two or more values are equal.
    
    *Example* See if a user's `role` field is set to `administrator`. 
    
        r.table('users').get(1)['role'].eq('administrator').run(conn)
        # alternative syntax
        (r.table('users').get(1)['role'] == 'administrator').run(conn)
    
    *Example* See if three variables contain equal values.
    
        r.eq(a, b, c).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.__ge__()
    '''value.ge(value[, value, ...]) -> bool
    value >= value -> bool
    
    Compare values, testing if the left-hand value is greater or equal to than the right-hand.
    
    *Example* Test if a player has scored 10 points or more.
    
        r.table('players').get(1)['score'].ge(10).run(conn)
        # alternative syntax
        (r.table('players').get(1)['score'] >= 10).run(conn)
    
    *Example* Test if variables are ordered from lowest to highest.
    
        a = 10
        b = 20
        c = 15
        r.ge(a, b, c).run(conn)
    
    This is the equivalent of the following:
    
        r.ge(a, b).and(r.ge(b, c)).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.__getitem__()
    '''sequence[attr] -> sequence
    singleSelection[attr] -> value
    object[attr] -> value
    array[index] -> value
    
    Get a single field from an object. If called on a sequence, gets that field from every object in the sequence, skipping objects that lack it.
    
    *Example* What was Iron Man's first appearance in a comic?
    
        r.table('marvel').get('IronMan')['firstAppearance'].run(conn)
    
    <!-- stop -->
    
    The `[]` command also accepts integer arguments as array offsets, like the [nth](http://rethinkdb.com/api/python/nth) command.
    
    *Example* Get the fourth element in a sequence. (The first element is position `0`, so the fourth element is position `3`.)
    
        r.expr([10, 20, 30, 40, 50])[3]
        
        40
    "'''
def rethinkdb.ast.RqlQuery.__gt__()
    '''value.gt(value[, value, ...]) -> bool
    value > value -> bool
    
    Compare values, testing if the left-hand value is greater than the right-hand.
    
    *Example* Test if a player has scored more than 10 points.
    
        r.table('players').get(1)['score'].gt(10).run(conn)
        # alternative syntax
        (r.table('players').get(1)['score'] > 10).run(conn)
    
    *Example* Test if variables are ordered from lowest to highest, with no values being equal to one another.
    
        a = 10
        b = 20
        c = 15
        r.gt(a, b, c).run(conn)
    
    This is the equivalent of the following:
    
        r.gt(a, b).and(r.gt(b, c)).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.__invert__()
    '''bool.not_() -> bool
    not_(bool) -> bool
    (~bool) -> bool
    
    Compute the logical inverse (not) of an expression.
    
    `not_` can be called either via method chaining, immediately after an expression that evaluates as a boolean value, or by passing the expression as a parameter to `not_`.  All values that are not `False` or `None` will be converted to `True`.
    
    You may also use `~` as a shorthand operator.
    
    *Example* Not true is false.
    
        r.not_(True).run(conn)
        r.expr(True).not_().run(conn)
        (~r.expr(True)).run(conn)
    
    These evaluate to `false`.
    
    Note that when using `~` the expression is wrapped in parentheses. Without this, Python will evaluate `r.expr(True)` *first* rather than using the ReQL operator and return an incorrect value. (`~True` evaluates to &minus;2 in Python.)
    
    *Example* Return all the users that do not have a "flag" field.
    
        r.table(\'users\').filter(
            lambda users: (~users.has_fields(\'flag\'))
        ).run(conn)
    
    *Example* As above, but prefix-style.
    
        r.table(\'users\').filter(
            lambda users: r.not_(users.has_fields(\'flag\'))
        ).run(conn)
    '''
def rethinkdb.ast.RqlQuery.__le__()
    '''value.le(value[, value, ...]) -> bool
    value <= value -> bool
    
    Compare values, testing if the left-hand value is less than or equal to the right-hand.
    
    *Example* Test if a player has scored 10 points or less.
    
        r.table('players').get(1)['score'].le(10).run(conn)
        # alternative syntax
        (r.table('players').get(1)['score'] <= 10).run(conn)
    
    *Example* Test if variables are ordered from highest to lowest.
    
        a = 20
        b = 10
        c = 15
        r.le(a, b, c).run(conn)
    
    This is the equivalent of the following:
    
        r.le(a, b).and(r.le(b, c)).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.__lt__()
    '''value.lt(value[, value, ...]) -> bool
    value < value -> bool
    
    Compare values, testing if the left-hand value is less than the right-hand.
    
    *Example* Test if a player has scored less than 10 points.
    
        r.table('players').get(1)['score'].lt(10).run(conn)
        # alternative syntax
        (r.table('players').get(1)['score'] < 10).run(conn)
    
    *Example* Test if variables are ordered from highest to lowest, with no values being equal to one another.
    
        a = 20
        b = 10
        c = 15
        r.lt(a, b, c).run(conn)
    
    This is the equivalent of the following:
    
        r.lt(a, b).and(r.lt(b, c)).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.__mod__()
    '''number % number -> number
    
    Find the remainder when dividing two numbers.
    
    *Example* It's as easy as 2 % 2 = 0.
    
        (r.expr(2) % 2).run(conn)
    
    `
    "'''
def rethinkdb.ast.RqlQuery.__mul__()
    '''number * number -> number
    array * number -> array
    number.mul(number[, number, ...]) -> number
    array.mul(number[, number, ...]) -> array
    
    Multiply two numbers, or make a periodic array.
    
    *Example* It\'s as easy as 2 * 2 = 4.
    
        (r.expr(2) * 2).run(conn)
    
    *Example* Arrays can be multiplied by numbers as well.
    
        (r.expr(["This", "is", "the", "song", "that", "never", "ends."]) * 100).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.__ne__()
    '''value.ne(value[, value, ...]) -> bool
    value != value -> bool
    
    Test if two or more values are not equal.
    
    *Example* See if a user's `role` field is not set to `administrator`. 
    
        r.table('users').get(1)['role'].ne('administrator').run(conn)
        # alternative syntax
        (r.table('users').get(1)['role'] != 'administrator').run(conn)
    
    *Example* See if three variables do not contain equal values.
    
        r.ne(a, b, c).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.__or__()
    '''bool | bool -> bool
    bool.or_([bool, bool, ...]) -> bool
    r.or_([bool, bool, ...]) -> bool
    
    Compute the logical "or" of one or more values.
    
    The `or_` command can be used as an infix operator after its first argument (`r.expr(True).or_(False)`) or given all of its arguments as parameters (`r.or_(True, False)`). The standard Python or operator, `|`, may also be used with ReQL.
    
    Calling `or_` with zero arguments will return `False`.
    
    *Example* Return whether either `a` or `b` evaluate to true.
    
        > a = True
        > b = False
        > (r.expr(a) | b).run(conn)
        
        True
    
    *Example* Return whether any of `x`, `y` or `z` evaluate to true.
    
        > x = False
        > y = False
        > z = False
        > r.or_(x, y, z).run(conn)
        
        False
    
    __Note:__ When using `or` inside a `filter` predicate to test the values of fields that may not exist on the documents being tested, you should use the `default` command with those fields so they explicitly return `False`.
    
        r.table(\'posts\').filter(lambda post:
            post[\'category\'].default(\'foo\').eq(\'article\').or(
                post[\'genre\'].default(\'foo\').eq(\'mystery\'))
        ).run(conn)
    '''
def rethinkdb.ast.RqlQuery.__sub__()
    '''number - number -> number
    time - number -> time
    time - time -> number
    number.sub(number[, number, ...]) -> number
    time.sub(number[, number, ...]) -> time
    time.sub(time) -> number
    
    Subtract two numbers.
    
    *Example* It's as easy as 2 - 2 = 0.
    
        (r.expr(2) - 2).run(conn)
    
    *Example* Create a date one year ago today.
    
        r.now() - 365*24*60*60
    
    *Example* Retrieve how many seconds elapsed between today and `date`.
    
        r.now() - date
    
    "'''
def rethinkdb.ast.RqlQuery.append()
    '''array.append(value) -> array
    
    Append a value to an array.
    
    *Example* Retrieve Iron Man's equipment list with the addition of some new boots.
    
        r.table('marvel').get('IronMan')['equipment'].append('newBoots').run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.avg()
    '''sequence.avg([field | function]) -> number
    
    Averages all the elements of a sequence.  If called with a field name,
    averages all the values of that field in the sequence, skipping
    elements of the sequence that lack that field.  If called with a
    function, calls that function on every element of the sequence and
    averages the results, skipping elements of the sequence where that
    function returns `None` or a non-existence error.
    
    Produces a non-existence error when called on an empty sequence.  You
    can handle this case with `default`.
    
    *Example* What's the average of 3, 5, and 7?
    
        r.expr([3, 5, 7]).avg().run(conn)
    
    *Example* What's the average number of points scored in a game?
    
        r.table('games').avg('points').run(conn)
    
    *Example* What's the average number of points scored in a game,
    counting bonus points?
    
        r.table('games').avg(lambda game:
            game['points'] + game['bonus_points']
        ).run(conn)
    
    *Example* What's the average number of points scored in a game?
    (But return `None` instead of raising an error if there are no games where
    points have been scored.)
    
        r.table('games').avg('points').default(None).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.ceil()
    '''r.ceil(number) -> number
    number.ceil() -> number
    
    Rounds the given value up, returning the smallest integer value greater than or equal to the given value (the value's ceiling).
    
    *Example* Return the ceiling of 12.345.
    
        > r.ceil(12.345).run(conn)
        
        13.0
    
    The `ceil` command can also be chained after an expression.
    
    *Example* Return the ceiling of -12.345.
    
        > r.expr(-12.345).ceil().run(conn)
        
        -12.0
    
    *Example* Return Iron Man's weight, rounded up with `ceil`.
    
        r.table('superheroes').get('ironman')['weight'].ceil().run(conn)
    "'''
def rethinkdb.ast.RqlQuery.change_at()
    '''array.change_at(index, value) -> array
    
    Change a value in an array at a given index. Returns the modified array.
    
    *Example* Bruce Banner hulks out.
    
        r.expr(["Iron Man", "Bruce", "Spider-Man"]).change_at(1, "Hulk").run(conn)
    '''
def rethinkdb.ast.RqlQuery.changes()
    '''stream.changes([options]) -> stream
    singleSelection.changes([options]) -> stream
    
    Turn a query into a changefeed, an infinite stream of objects representing changes to the query\'s results as they occur. A changefeed may return changes to a table or an individual document (a "point" changefeed). Commands such as `filter` or `map` may be used before the `changes` command to transform or filter the output, and many commands that operate on sequences can be chained after `changes`.
    
    There are four optional arguments to `changes`.
    
    * `squash`: Controls how change notifications are batched. Acceptable values are `True`, `False` and a numeric value:
        * `True`: When multiple changes to the same document occur before a batch of notifications is sent, the changes are "squashed" into one change. The client receives a notification that will bring it fully up to date with the server.
        * `False`: All changes will be sent to the client verbatim. This is the default.
        * `n`: A numeric value (floating point). Similar to `True`, but the server will wait `n` seconds to respond in order to squash as many changes together as possible, reducing network traffic. The first batch will always be returned immediately.
    * `changefeed_queue_size`: the number of changes the server will buffer between client reads before it starts dropping changes and generates an error (default: 100,000).
    * `include_initial`: if `True`, the changefeed stream will begin with the current contents of the table or selection being monitored. These initial results will have `new_val` fields, but no `old_val` fields. The initial results may be intermixed with actual changes, as long as an initial result for the changed document has already been given. If an initial result for a document has been sent and a change is made to that document that would move it to the unsent part of the result set (e.g., a changefeed monitors the top 100 posters, the first 50 have been sent, and poster 48 has become poster 52), an "uninitial" notification will be sent, with an `old_val` field but no `new_val` field.
    * `include_states`: if `True`, the changefeed stream will include special status documents consisting of the field `state` and a string indicating a change in the feed\'s state. These documents can occur at any point in the feed between the notification documents described below. If `include_states` is `False` (the default), the status documents will not be sent.
    * `include_offsets`: if `True`, a changefeed stream on an `order_by.limit` changefeed will include `old_offset` and `new_offset` fields in status documents that include `old_val` and `new_val`. This allows applications to maintain ordered lists of the stream\'s result set. If `old_offset` is set and not `None`, the element at `old_offset` is being deleted; if `new_offset` is set and not `None`, then `new_val` is being inserted at `new_offset`. Setting `include_offsets` to `True` on a changefeed that does not support it will raise an error.
    
    There are currently two states:
    
    * `{"state": "initializing"}` indicates the following documents represent initial values on the feed rather than changes. This will be the first document of a feed that returns initial values.
    * `{"state": "ready"}` indicates the following documents represent changes. This will be the first document of a feed that does *not* return initial values; otherwise, it will indicate the initial values have all been sent.
    
    If the table becomes unavailable, the changefeed will be disconnected, and a runtime exception will be thrown by the driver.
    
    Changefeed notifications take the form of a two-field object:
    
        {
            "old_val": <document before change>,
            "new_val": <document after change>
        }
    
    When a document is deleted, `new_val` will be `None`; when a document is inserted, `old_val` will be `None`.
    
    The server will buffer up to 100,000 elements. If the buffer limit is hit, early changes will be discarded, and the client will receive an object of the form `{"error": "Changefeed cache over array size limit, skipped X elements."}` where `X` is the number of elements skipped.
    
    Commands that operate on streams (such as [filter](http://rethinkdb.com/api/python/filter/) or [map](http://rethinkdb.com/api/python/map/)) can usually be chained after `changes`.  However, since the stream produced by `changes` has no ending, commands that need to consume the entire stream before returning (such as [reduce](http://rethinkdb.com/api/python/reduce/) or [count](http://rethinkdb.com/api/python/count/)) cannot.
    
    *Example* Subscribe to the changes on a table.
    
    Start monitoring the changefeed in one client:
    
        for change in r.table(\'games\').changes().run(conn):
          print change
    
    As these queries are performed in a second client, the first client would receive and print the following objects:
    
        > r.table(\'games\').insert({\'id\': 1}).run(conn)
        {\'old_val\': None, \'new_val\': {\'id\': 1}}
        
        > r.table(\'games\').get(1).update({\'player1\': \'Bob\'}).run(conn)
        {\'old_val\': {\'id\': 1}, \'new_val\': {\'id\': 1, \'player1\': \'Bob\'}}
        
        > r.table(\'games\').get(1).replace({\'id\': 1, \'player1\': \'Bob\', \'player2\': \'Alice\'}).run(conn)
        {\'old_val\': {\'id\': 1, \'player1\': \'Bob\'},
         \'new_val\': {\'id\': 1, \'player1\': \'Bob\', \'player2\': \'Alice\'}}
        
        > r.table(\'games\').get(1).delete().run(conn)
        {\'old_val\': {\'id\': 1, \'player1\': \'Bob\', \'player2\': \'Alice\'}, \'new_val\': None}
        
        > r.table_drop(\'games\').run(conn)
        ReqlRuntimeError: Changefeed aborted (table unavailable)
    
    *Example* Return all the changes that increase a player\'s score.
    
        r.table(\'test\').changes().filter(
          r.row[\'new_val\'][\'score\'] > r.row[\'old_val\'][\'score\']
        ).run(conn)
    
    *Example* Return all the changes to a specific player\'s score that increase it past 10.
    
        r.table(\'test\').get(1).filter(r.row[\'score\'].gt(10)).changes().run(conn)
    
    *Example* Return all the inserts on a table.
    
        r.table(\'test\').changes().filter(r.row[\'old_val\'].eq(None)).run(conn)
    
    *Example* Return all the changes to game 1, with state notifications and initial values.
    
        r.table(\'games\').get(1).changes(include_initial=True, include_states=True).run(conn)
        
        # result returned on changefeed
        {"state": "initializing"}
        {"new_val": {"id": 1, "score": 12, "arena": "Hobbiton Field"}}
        {"state": "ready"}
        {
        \t"old_val": {"id": 1, "score": 12, "arena": "Hobbiton Field"},
        \t"new_val": {"id": 1, "score": 14, "arena": "Hobbiton Field"}
        }
        {
        \t"old_val": {"id": 1, "score": 14, "arena": "Hobbiton Field"},
        \t"new_val": {"id": 1, "score": 17, "arena": "Hobbiton Field", "winner": "Frodo"}
        }
    
    *Example* Return all the changes to the top 10 games. This assumes the presence of a `score` secondary index on the `games` table.
    
        r.table(\'games\').order_by(index=r.desc(\'score\')).limit(10).changes().run(conn)
    '''
def rethinkdb.ast.RqlQuery.coerce_to()
    '''sequence.coerce_to('array') -> array
    value.coerce_to('string') -> string
    string.coerce_to('number') -> number
    array.coerce_to('object') -> object
    sequence.coerce_to('object') -> object
    object.coerce_to('array') -> array
    binary.coerce_to('string') -> string
    string.coerce_to('binary') -> binary
    
    Convert a value of one type into another.
    
    * a sequence, selection or object can be coerced to an array
    * a sequence, selection or an array of key-value pairs can be coerced to an object
    * a string can be coerced to a number
    * any datum (single value) can be coerced to a string
    * a binary object can be coerced to a string and vice-versa
    
    *Example* Coerce a stream to an array to store its output in a field. (A stream cannot be stored in a field directly.)
    
        r.table('posts').map(lambda post: post.merge(
            { 'comments': r.table('comments').get_all(post['id'], index='post_id').coerce_to('array') }
        )).run(conn)
    
    *Example* Coerce an array of pairs into an object.
    
        r.expr([['name', 'Ironman'], ['victories', 2000]]).coerce_to('object').run(conn)
    
    __Note:__ To coerce a list of key-value pairs like `['name', 'Ironman', 'victories', 2000]` to an object, use the [object](http://rethinkdb.com/api/python/object) command.
    
    *Example* Coerce a number to a string.
    
        r.expr(1).coerce_to('string').run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.concat_map()
    '''stream.concat_map(function) -> stream
    array.concat_map(function) -> array
    
    Concatenate one or more elements into a single sequence using a mapping function.
    
    `concat_map` works in a similar fashion to [map](http://rethinkdb.com/api/python/map/), applying the given function to each element in a sequence, but it will always return a single sequence. If the mapping function returns a sequence, `map` would produce a sequence of sequences:
    
        r.expr([1, 2, 3]).map(lambda x: [x, x.mul(2)]).run(conn)
    
    Result:
    
        [[1, 2], [2, 4], [3, 6]]
    
    Whereas `concat_map` with the same mapping function would merge those sequences into one:
    
        r.expr([1, 2, 3]).concat_map(lambda x: [x, x.mul(2)]).run(conn)
    
    Result:
    
        [1, 2, 2, 4, 3, 6]
    
    The return value, array or stream, will be the same type as the input.
    
    *Example* Construct a sequence of all monsters defeated by Marvel heroes. The field "defeatedMonsters" is an array of one or more monster names.
    
        r.table(\'marvel\').concat_map(lambda hero: hero[\'defeatedMonsters\']).run(conn)
    
    *Example* Simulate an [eq_join](http://rethinkdb.com/api/python/eq_join/) using `concat_map`. (This is how ReQL joins are implemented internally.)
    
        r.table(\'posts\').concat_map(
            lambda post: r.table(\'comments\').get_all(
                post[\'id\'], index=\'post_id\'
            ).map(
                lambda comment: { \'left\': post, \'right\': comment}
            )
        ).run(conn)
    '''
def rethinkdb.ast.RqlQuery.contains()
    '''sequence.contains([value | predicate_function, ...]) -> bool
    
    When called with values, returns `True` if a sequence contains all the
    specified values.  When called with predicate functions, returns `True`
    if for each predicate there exists at least one element of the stream
    where that predicate returns `True`.
    
    Values and predicates may be mixed freely in the argument list.
    
    *Example* Has Iron Man ever fought Superman?
    
        r.table('marvel').get('ironman')['opponents'].contains('superman').run(conn)
    
    *Example* Has Iron Man ever defeated Superman in battle?
    
        r.table('marvel').get('ironman')['battles'].contains(lambda battle:
            (battle['winner'] == 'ironman') & (battle['loser'] == 'superman')
        ).run(conn)
    
    *Example* Use `contains` with a predicate function to simulate an `or`. Return the Marvel superheroes who live in Detroit, Chicago or Hoboken.
    
        r.table('marvel').filter(
            lambda hero: r.expr(['Detroit', 'Chicago', 'Hoboken']).contains(hero['city'])
        ).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.count()
    '''sequence.count([value | predicate_function]) -> number
    binary.count() -> number
    string.count() -> number
    object.count() -> number
    
    Counts the number of elements in a sequence or key/value pairs in an object, or returns the size of a string or binary object.
    
    When `count` is called on a sequence with a predicate value or function, it returns the number of elements in the sequence equal to that value or where the function returns `True`. On a [binary](http://rethinkdb.com/api/python/binary) object, `count` returns the size of the object in bytes; on strings, `count` returns the string's length. This is determined by counting the number of Unicode codepoints in the string, counting combining codepoints separately.
    
    *Example* Count the number of users.
    
        r.table('users').count().run(conn)
    
    *Example* Count the number of 18 year old users.
    
        r.table('users')['age'].count(18).run(conn)
    
    *Example* Count the number of users over 18.
    
        r.table('users')['age'].count(lambda age: age > 18).run(conn)
    
        r.table('users').count(lambda user: user['age'] > 18).run(conn)
    
    *Example* Return the length of a Unicode string.
    
        > r.expr(u'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf').count().run(conn)
        5
    "'''
def rethinkdb.ast.RqlQuery.date()
    '''time.date() -> time
    
    Return a new time object only based on the day, month and year (ie. the same day at 00:00).
    
    *Example* Retrieve all the users whose birthday is today.
    
        r.table("users").filter(lambda user:
            user["birthdate"].date() == r.now().date()
        ).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.day()
    '''time.day() -> number
    
    Return the day of a time object as a number between 1 and 31.
    
    *Example* Return the users born on the 24th of any month.
    
        r.table("users").filter(
            r.row["birthdate"].day() == 24
        )
    
    '''
def rethinkdb.ast.RqlQuery.day_of_week()
    '''time.day_of_week() -> number
    
    Return the day of week of a time object as a number between 1 and 7 (following ISO 8601 standard). For your convenience, the terms r.monday, r.tuesday etc. are defined and map to the appropriate integer.
    
    *Example* Return today\'s day of week.
    
        r.now().day_of_week().run(conn)
    
    *Example* Retrieve all the users who were born on a Tuesday.
    
        r.table("users").filter( lambda user:
            user["birthdate"].day_of_week().eq(r.tuesday)
        )
    
    '''
def rethinkdb.ast.RqlQuery.day_of_year()
    '''time.day_of_year() -> number
    
    Return the day of the year of a time object as a number between 1 and 366 (following ISO 8601 standard).
    
    *Example* Retrieve all the users who were born the first day of a year.
    
        r.table("users").filter(
            r.row["birthdate"].day_of_year() == 1
        ).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.default()
    '''value.default(default_value | function) -> any
    sequence.default(default_value | function) -> any
    
    Provide a default value in case of non-existence errors. The `default` command evaluates its first argument (the value it\'s chained to). If that argument returns `None` or a non-existence error is thrown in evaluation, then `default` returns its second argument. The second argument is usually a default value, but it can be a function that returns a value.
    
    *Example* Retrieve the titles and authors of the table `posts`.
    In the case where the author field is missing or `None`, we want to retrieve the string
    `Anonymous`.
    
        r.table("posts").map(lambda post:
            {
                "title": post["title"],
                "author": post["author"].default("Anonymous")
            }
        ).run(conn)
    
    <!-- stop -->
    
    We can rewrite the previous query with `r.branch` too.
    
        r.table("posts").map(lambda post:
            r.branch(
                post.has_fields("author"),
                {
                    "title": post["title"],
                    "author": post["author"]
                },
                {
                    "title": post["title"],
                    "author": "Anonymous" 
                }
            )
        ).run(conn)
    
    *Example* The `default` command can also be used to filter documents. Retrieve all our users who are not grown-ups or whose age is unknown
    (i.e., the field `age` is missing or equals `None`).
    
        r.table("users").filter(lambda user:
            (user["age"] < 18).default(True)
        ).run(conn)
    
    One more way to write the previous query is to set the age to be `-1` when the
    field is missing.
    
        r.table("users").filter(lambda user:
            user["age"].default(-1) < 18
        ).run(conn)
    
    This can be accomplished with [has_fields](http://rethinkdb.com/api/python/has_fields/) rather than `default`.
    
        r.table("users").filter(lambda user:
            user.has_fields("age").not_() | (user["age"] < 18)
        ).run(conn)
    
    The body of every [filter](http://rethinkdb.com/api/python/filter/) is wrapped in an implicit `.default(False)`. You can overwrite the value `False` with the `default` option.
    
        r.table("users").filter(
            lambda user: (user["age"] < 18).default(True),
            default=True
        ).run(conn)
    
    *Example* The function form of `default` receives the error message as its argument.
    
        r.table("posts").map(lambda post:
            {
                "title": post["title"],
                "author": post["author"].default(lambda err: err)
            }
        ).run(conn)
    
    This particular example simply returns the error message, so it isn\'t very useful. But it would be possible to change the default value based on the specific error message thrown.
    '''
def rethinkdb.ast.RqlQuery.delete_at()
    '''array.delete_at(index [,endIndex]) -> array
    
    Remove one or more elements from an array at a given index. Returns the modified array. (Note: `delete_at` operates on arrays, not documents; to delete documents, see the [delete](http://rethinkdb.com/api/python/delete) command.)
    
    If only `index` is specified, `delete_at` removes the element at that index. If both `index` and `end_index` are specified, `delete_at` removes the range of elements between `index` and `end_index`, inclusive of `index` but not inclusive of `end_index`.
    
    If `end_index` is specified, it must not be less than `index`. Both `index` and `end_index` must be within the array's bounds (i.e., if the array has 10 elements, an `index` or `end_index` of 10 or higher is invalid).
    
    By using a negative `index` you can delete from the end of the array. `-1` is the last element in the array, `-2` is the second-to-last element, and so on. You may specify a negative `end_index`, although just as with a positive value, this will not be inclusive. The range `(2,-1)` specifies the third element through the next-to-last element.
    
    *Example* Delete the second element of an array.
    
        > r.expr(['a','b','c','d','e','f']).delete_at(1).run(conn)
        
        ['a', 'c', 'd', 'e', 'f']
    
    *Example* Delete the second and third elements of an array.
    
        > r.expr(['a','b','c','d','e','f']).delete_at(1,3).run(conn)
        
        ['a', 'd', 'e', 'f']
    
    *Example* Delete the next-to-last element of an array.
    
        > r.expr(['a','b','c','d','e','f']).delete_at(-2).run(conn)
        
        ['a', 'b', 'c', 'd', 'f']
    
    *Example* Delete a comment on a post.
    
    Given a post document such as:
    
    {
        id: '4cf47834-b6f9-438f-9dec-74087e84eb63',
        title: 'Post title',
        author: 'Bob',
        comments: [
            { author: 'Agatha', text: 'Comment 1' },
            { author: 'Fred', text: 'Comment 2' }
        ]
    }
    
    The second comment can be deleted by using `update` and `delete_at` together.
    
        r.table('posts').get('4cf47834-b6f9-438f-9dec-74087e84eb63').update(
            lambda post: { 'comments': post['comments'].delete_at(1) }
        ).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.difference()
    '''array.difference(array) -> array
    
    Remove the elements of one array from another array.
    
    *Example* Retrieve Iron Man's equipment list without boots.
    
        r.table('marvel').get('IronMan')['equipment'].difference(['Boots']).run(conn)
    
    *Example* Remove Iron Man's boots from his equipment.
    
        r.table('marvel').get('IronMan')['equipment'].update(lambda doc:
            {'equipment': doc['equipment'].difference(['Boots'])}
        ).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.distance()
    '''geometry.distance(geometry[, geo_system='WGS84', unit='m']) -> number
    r.distance(geometry, geometry[, geo_system='WGS84', unit='m']) -> number
    
    Compute the distance between a point and another geometry object. At least one of the geometry objects specified must be a point.
    
    Optional arguments available with `distance` are:
    
    * `geo_system`: the reference ellipsoid to use for geographic coordinates. Possible values are `WGS84` (the default), a common standard for Earth's geometry, or `unit_sphere`, a perfect sphere of 1 meter radius.
    * `unit`: Unit to return the distance in. Possible values are `m` (meter, the default), `km` (kilometer), `mi` (international mile), `nm` (nautical mile), `ft` (international foot).
    
    If one of the objects is a polygon or a line, the point will be projected onto the line or polygon assuming a perfect sphere model before the distance is computed (using the model specified with `geo_system`). As a consequence, if the polygon or line is extremely large compared to Earth's radius and the distance is being computed with the default WGS84 model, the results of `distance` should be considered approximate due to the deviation between the ellipsoid and spherical models.
    
    *Example* Compute the distance between two points on the Earth in kilometers.
    
        > point1 = r.point(-122.423246, 37.779388)
        > point2 = r.point(-117.220406, 32.719464)
        > r.distance(point1, point2, unit='km').run(conn)
        
        734.1252496021841
    "'''
def rethinkdb.ast.RqlQuery.distinct()
    '''sequence.distinct() -> array
    table.distinct([index=<indexname>]) -> stream
    
    Removes duplicate elements from a sequence.
    
    The `distinct` command can be called on any sequence or table with an index.
    
    *Example* Which unique villains have been vanquished by Marvel heroes?
    
        r.table('marvel').concat_map(
            lambda hero: hero['villain_list']).distinct().run(conn)
    
    *Example* Topics in a table of messages have a secondary index on them, and more than one message can have the same topic. What are the unique topics in the table?
    
        r.table('messages').distinct(index='topics').run(conn)
    
    The above structure is functionally identical to:
    
        r.table('messages')['topics'].distinct().run(conn)
    
    However, the first form (passing the index as an argument to `distinct`) is faster, and won't run into array limit issues since it's returning a stream.
    "'''
def rethinkdb.ast.RqlQuery.do()
    '''any.do(function) -> any
    r.do([args]*, function) -> any
    any.do(expr) -> any
    r.do([args]*, expr) -> any
    
    Call an anonymous function using return values from other ReQL commands or queries as arguments.
    
    The last argument to `do` (or, in some forms, the only argument) is an expression or an anonymous function which receives values from either the previous arguments or from prefixed commands chained before `do`. The `do` command is essentially a single-element [map](http://rethinkdb.com/api/python/map/), letting you map a function over just one document. This allows you to bind a query result to a local variable within the scope of `do`, letting you compute the result just once and reuse it in a complex expression or in a series of ReQL commands.
    
    Arguments passed to the `do` function must be basic data types, and cannot be streams or selections. (Read about [ReQL data types](http://rethinkdb.com/docs/data-types/).) While the arguments will all be evaluated before the function is executed, they may be evaluated in any order, so their values should not be dependent on one another. The type of `do`'s result is the type of the value returned from the function or last expression.
    
    *Example* Compute a golfer's net score for a game.
    
        r.table('players').get('86be93eb-a112-48f5-a829-15b2cb49de1d').do(
            lambda player: player['gross_score'] - player['course_handicap']
        ).run(conn)
    
    *Example* Return the name of the best scoring player in a two-player golf match.
    
        r.do(r.table('players').get(id1), r.table('players').get(id2),
            (lambda player1, player2:
                r.branch(player1['gross_score'].lt(player2['gross_score']),
                player1, player2))
        ).run(conn)
    
    Note that `branch`, the ReQL conditional command, must be used instead of `if`. See the `branch` [documentation](http://rethinkdb.com/api/python/branch) for more.
    
    *Example* Take different actions based on the result of a ReQL [insert](http://rethinkdb.com/api/python/insert) command.
    
        new_data = {
            'id': 100,
            'name': 'Agatha',
            'gross_score': 57,
            'course_handicap': 4
        }
        r.table('players').insert(new_data).do(lambda doc:
            r.branch((doc['inserted'] != 0),
                r.table('log').insert({'time': r.now(), 'response': doc, 'result': 'ok'}),
                r.table('log').insert({'time': r.now(), 'response': doc, 'result': 'error'}))
        ).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.downcase()
    '''string.downcase() -> string
    
    Lowercases a string.
    
    *Example*
    
        > r.expr("Sentence about LaTeX.").downcase().run(conn)
        "sentence about latex."
    
    __Note:__ `upcase` and `downcase` only affect ASCII characters.
    '''
def rethinkdb.ast.RqlQuery.during()
    '''time.during(start_time, end_time[, left_bound="closed", right_bound="open"])
        -> bool
    
    Return whether a time is between two other times.
    
    By default, this is inclusive of the start time and exclusive of the end time. Set `left_bound` and `right_bound` to explicitly include (`closed`) or exclude (`open`) that endpoint of the range.
    
    *Example* Retrieve all the posts that were posted between December 1st, 2013 (inclusive) and December 10th, 2013 (exclusive).
    
        r.table("posts").filter(
            r.row[\'date\'].during(r.time(2013, 12, 1, "Z"), r.time(2013, 12, 10, "Z"))
        ).run(conn)
    
    *Example* Retrieve all the posts that were posted between December 1st, 2013 (exclusive) and December 10th, 2013 (inclusive).
    
        r.table("posts").filter(
            r.row[\'date\'].during(r.time(2013, 12, 1, "Z"), r.time(2013, 12, 10, "Z"), left_bound="open", right_bound="closed")
        ).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.eq()
    '''value.eq(value[, value, ...]) -> bool
    value == value -> bool
    
    Test if two or more values are equal.
    
    *Example* See if a user's `role` field is set to `administrator`. 
    
        r.table('users').get(1)['role'].eq('administrator').run(conn)
        # alternative syntax
        (r.table('users').get(1)['role'] == 'administrator').run(conn)
    
    *Example* See if three variables contain equal values.
    
        r.eq(a, b, c).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.eq_join()
    '''sequence.eq_join(left_field, right_table[, index=\'id\', ordered=False]) -> sequence
    sequence.eq_join(predicate_function, right_table[, index=\'id\', ordered=False]) -> sequence
    
    Join tables using a field or function on the left-hand sequence matching primary keys or secondary indexes on the right-hand table. `eq_join` is more efficient than other ReQL join types, and operates much faster. Documents in the result set consist of pairs of left-hand and right-hand documents, matched when the field on the left-hand side exists and is non-null and an entry with that field\'s value exists in the specified index on the right-hand side.
    
    The result set of `eq_join` is a stream or array of objects. Each object in the returned set will be an object of the form `{ left: <left-document>, right: <right-document> }`, where the values of `left` and `right` will be the joined documents. Use the <code><a href="/api/python/zip/">zip</a></code> command to merge the `left` and `right` fields together.
    
    The results from `eq_join` are, by default, not ordered. The optional `ordered=True` parameter will cause `eq_join` to order the output based on the left side input stream. (If there are multiple matches on the right side for a document on the left side, their order is not guaranteed even if `ordered` is `True`.) Requiring ordered results can significantly slow down `eq_join`, and in many circumstances this ordering will not be required. (See the first example, in which ordered results are obtained by using `order_by` after `eq_join`.)
    
    Suppose the players table contains these documents:
    
        [
            { \'id\': 1, \'player\': \'George\', \'gameId\': 1 },
            { \'id\': 2, \'player\': \'Agatha\', \'gameId\': 3 },
            { \'id\': 3, \'player\': \'Fred\', \'gameId\': 2 },
            { \'id\': 4, \'player\': \'Marie\', \'gameId\': 2 },
            { \'id\': 5, \'player\': \'Earnest\', \'gameId\': 1 },
            { \'id\': 6, \'player\': \'Beth\', \'gameId\': 3 }
        ]
    
    The games table contains these documents:
    
        [
            { \'id\': 1, \'field\': \'Little Delving\' },
            { \'id\': 2, \'field\': \'Rushock Bog\' },
            { \'id\': 3, \'field\': \'Bucklebury\' }
        ]
    
    **Example:** Match players with the games they\'ve played against one another.
    
    Join these tables using `game_id` on the player table and `id` on the games table:
    
        r.table(\'players\').eq_join(\'game_id\', r.table(\'games\')).run(conn)
    
    This will return a result set such as the following:
    
        [
            {
                "left" : { "gameId" : 3, "id" : 2, "player" : "Agatha" },
                "right" : { "id" : 3, "field" : "Bucklebury" }
            },
            {
                "left" : { "gameId" : 2, "id" : 3, "player" : "Fred" },
                "right" : { "id" : 2, "field" : "Rushock Bog" }
            },
            ...
        ]
    
    <!-- stop -->
    
    What you likely want is the result of using `zip` with that. For clarity, we\'ll use `without` to drop the `id` field from the games table (it conflicts with the `id` field for the players and it\'s redundant anyway), and we\'ll order it by the games.
    
        r.table(\'players\').eq_join(\'game_id\', r.table(\'games\')).without({\'right\': "id"}).zip().order_by(\'game_id\').run(conn)
        
        [
            { "field": "Little Delving", "gameId": 1, "id": 5, "player": "Earnest" },
            { "field": "Little Delving", "gameId": 1, "id": 1, "player": "George" },
            { "field": "Rushock Bog", "gameId": 2, "id": 3, "player": "Fred" },
            { "field": "Rushock Bog", "gameId": 2, "id": 4, "player": "Marie" },
            { "field": "Bucklebury", "gameId": 3, "id": 6, "player": "Beth" },
            { "field": "Bucklebury", "gameId": 3, "id": 2, "player": "Agatha" }
        ]
    
    For more information, see [Table joins in RethinkDB](http://rethinkdb.com/docs/table-joins/).
    
    **Example:** Use a secondary index on the right table rather than the primary key. If players have a secondary index on their cities, we can get a list of arenas with players in the same area.
    
        r.table(\'arenas\').eq_join(\'city_id\', r.table(\'arenas\'), index=\'city_id\').run(conn)
    
    **Example:** Use a nested key as the join field. Suppose the documents in the players table were structured like this:
    
        { \'id\': 1, \'player\': \'George\', \'game\': {\'id\': 1} },
        { \'id\': 2, \'player\': \'Agatha\', \'game\': {\'id\': 3} },
        ...
    
    Simply specify the field using the `row` command instead of a string.
    
        r.table(\'players\').eq_join(r.row[\'game\'][\'id\'], r.table(\'games\')).without({\'right\': \'id\'}).zip().run(conn)
        
        [
            { "field": "Little Delving", "game": { "id": 1 }, "id": 5, "player": "Earnest" },
            { "field": "Little Delving", "game": { "id": 1 }, "id": 1, "player": "George" },
            ...
        ]
    
    **Example:** Use a function instead of a field to join on a more complicated expression. Suppose the players have lists of favorite games ranked in order in a field such as `"favorites": [3, 2, 1]`. Get a list of players and their top favorite:
    
        r.table(\'players3\').eq_join(
            lambda player: player[\'favorites\'].nth(0),
            r.table(\'games\')
        ).without([{\'left\': [\'favorites\', \'game_id\', \'id\']}, {\'right\': \'id\'}]).zip()
    
    Result:
    
        [
        \t{ "field": "Rushock Bog", "name": "Fred" },
        \t{ "field": "Little Delving", "name": "George" },
        \t...
        ]
    '''
def rethinkdb.ast.RqlQuery.fill()
    '''line.fill() -> polygon
    
    Convert a Line object into a Polygon object. If the last point does not specify the same coordinates as the first point, `polygon` will close the polygon by connecting them.
    
    Longitude (&minus;180 to 180) and latitude (&minus;90 to 90) of vertices are plotted on a perfect sphere. See [Geospatial support](http://rethinkdb.com/docs/geo-support/) for more information on ReQL's coordinate system.
    
    If the last point does not specify the same coordinates as the first point, `polygon` will close the polygon by connecting them. You cannot directly construct a polygon with holes in it using `polygon`, but you can use [polygon_sub](http://rethinkdb.com/api/python/polygon_sub) to use a second polygon within the interior of the first to define a hole.
    
    *Example* Create a line object and then convert it to a polygon.
    
        r.table('geo').insert({
            'id': 201,
            'rectangle': r.line(
                [-122.423246, 37.779388],
                [-122.423246, 37.329898],
                [-121.886420, 37.329898],
                [-121.886420, 37.779388]
            )
        }).run(conn)
        
        r.table('geo').get(201).update({
            'rectangle': r.row['rectangle'].fill()
        }, non_atomic=True).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.filter()
    '''selection.filter(predicate_function[, default=False]) -> selection
    stream.filter(predicate_function[, default=False]) -> stream
    array.filter(predicate_function[, default=False]) -> array
    
    Return all the elements in a sequence for which the given predicate is true. The return value of `filter` will be the same as the input (sequence, stream, or array). Documents can be filtered in a variety of ways&mdash;ranges, nested values, boolean conditions, and the results of anonymous functions.
    
    By default, `filter` will silently skip documents with missing fields: if the predicate tries to access a field that doesn\'t exist (for instance, the predicate `{\'age\': 30}` applied to a document with no `age` field), that document will not be returned in the result set, and no error will be generated. This behavior can be changed with the `default` optional argument.
    
    * If `default` is set to `True`, documents with missing fields will be returned rather than skipped.
    * If `default` is set to `r.error()`, an `ReqlRuntimeError` will be thrown when a document with a missing field is tested.
    * If `default` is set to `False` (the default), documents with missing fields will be skipped.
    
    *Example* Get all users who are 30 years old.
    
        r.table(\'users\').filter({\'age\': 30}).run(conn)
    
    The predicate `{\'age\': 30}` selects documents in the `users` table with an `age` field whose value is `30`. Documents with an `age` field set to any other value *or* with no `age` field present are skipped.
    
    <!-- stop -->
    
    While the `{\'field\': value}` style of predicate is useful for exact matches, a more general way to write a predicate is to use the [row](http://rethinkdb.com/api/python/row) command with a comparison operator such as [eq](http://rethinkdb.com/api/python/eq) (`==`) or [gt](http://rethinkdb.com/api/python/gt) (`>`), or to use a lambda function that returns `True` or `False`.
    
        r.table(\'users\').filter(r.row["age"] == 30).run(conn)
    
    In this case, the predicate `r.row["age"] == 30` returns `True` if the field `age` is equal to 30. You can write this predicate as a lambda function instead:
    
        r.table(\'users\').filter(lambda user:
            user["age"] == 30
        ).run(conn)
    
    Predicates to `filter` are evaluated on the server, and must use ReQL expressions. Some Python comparison operators are overloaded by the RethinkDB driver and will be translated to ReQL, such as `==`, `<`/`>` and `|`/`&` (note the single character form, rather than `||`/`&&`).
    
    Also, predicates must evaluate document fields. They cannot evaluate [secondary indexes](http://rethinkdb.com/docs/secondary-indexes/).
    
    *Example* Get all users who are more than 18 years old.
    
        r.table("users").filter(r.row["age"] > 18).run(conn)
    
    *Example* Get all users who are less than 18 years old and more than 13 years old.
    
        r.table("users").filter((r.row["age"] < 18) & (r.row["age"] > 13)).run(conn)
    
    *Example* Get all users who are more than 18 years old or have their parental consent.
    
        r.table("users").filter(
            (r.row["age"] >= 18) | (r.row["hasParentalConsent"])).run(conn)
    
    *Example* Retrieve all users who subscribed between January 1st, 2012
    (included) and January 1st, 2013 (excluded).
    
        r.table("users").filter(
            lambda user: user["subscription_date"].during(
                r.time(2012, 1, 1, \'Z\'), r.time(2013, 1, 1, \'Z\'))
        ).run(conn)
    
    *Example* Retrieve all users who have a gmail account (whose field `email` ends with `@gmail.com`).
    
        r.table("users").filter(
            lambda user: user["email"].match("@gmail.com$")
        ).run(conn)
    
    *Example* Filter based on the presence of a value in an array.
    
    Given this schema for the `users` table:
    
        {
            "name": <type \'str\'>
            "places_visited": [<type \'str\'>]
        }
    
    Retrieve all users whose field `places_visited` contains `France`.
    
        r.table("users").filter(lambda user:
            user["places_visited"].contains("France")
        ).run(conn)
    
    *Example* Filter based on nested fields.
    
    Given this schema for the `users` table:
    
        {
            "id": <type \'str\'>
            "name": {
                "first": <type \'str\'>,
                "middle": <type \'str\'>,
                "last": <type \'str\'>
            }
        }
    
    Retrieve all users named "William Adama" (first name "William", last name
    "Adama"), with any middle name.
    
        r.table("users").filter({
            "name": {
                "first": "William",
                "last": "Adama"
            }
        }).run(conn)
    
    If you want an exact match for a field that is an object, you will have to use `r.literal`.
    
    Retrieve all users named "William Adama" (first name "William", last name
    "Adama"), and who do not have a middle name.
    
        r.table("users").filter(r.literal({
            "name": {
                "first": "William",
                "last": "Adama"
            }
        })).run(conn)
    
    You may rewrite these with lambda functions.
    
        r.table("users").filter(
            lambda user:
            (user["name"]["first"] == "William")
                & (user["name"]["last"] == "Adama")
        ).run(conn)
    
        r.table("users").filter(lambda user:
            user["name"] == {
                "first": "William",
                "last": "Adama"
            }
        ).run(conn)
    
    By default, documents missing fields tested by the `filter` predicate are skipped. In the previous examples, users without an `age` field are not returned. By passing the optional `default` argument to `filter`, you can change this behavior.
    
    *Example* Get all users less than 18 years old or whose `age` field is missing.
    
        r.table("users").filter(r.row["age"] < 18, default=True).run(conn)
    
    *Example* Get all users more than 18 years old. Throw an error if a
    document is missing the field `age`.
    
        r.table("users").filter(r.row["age"] > 18, default=r.error()).run(conn)
    
    *Example* Get all users who have given their phone number (all the documents whose field `phone_number` exists and is not `None`).
    
        r.table(\'users\').filter(
            lambda user: user.has_fields(\'phone_number\')
        ).run(conn)
    
    *Example* Get all users with an "editor" role or an "admin" privilege.
    
        r.table(\'users\').filter(
            lambda user: (user[\'role\'] == \'editor\').default(False) |
                (user[\'privilege\'] == \'admin\').default(False)
        ).run(conn)
    
    Instead of using the `default` optional argument to `filter`, we have to use default values on the fields within the `or` clause. Why? If the field on the left side of the `or` clause is missing from a document&mdash;in this case, if the user doesn\'t have a `role` field&mdash;the predicate will generate an error, and will return `False` (or the value the `default` argument is set to) without evaluating the right side of the `or`. By using `.default(False)` on the fields, each side of the `or` will evaluate to either the field\'s value or `False` if the field doesn\'t exist.
    '''
def rethinkdb.ast.RqlQuery.floor()
    '''r.floor(number) -> number
    number.floor() -> number
    
    Rounds the given value down, returning the largest integer value less than or equal to the given value (the value's floor).
    
    *Example* Return the floor of 12.345.
    
        > r.floor(12.345).run(conn)
        
        12.0
    
    The `floor` command can also be chained after an expression.
    
    *Example* Return the floor of -12.345.
    
        > r.expr(-12.345).floor().run(conn)
        
        -13.0
    
    *Example* Return Iron Man's weight, rounded down with `floor`.
    
        r.table('superheroes').get('ironman')['weight'].floor().run(conn)
    "'''
def rethinkdb.ast.RqlQuery.fold()
    '''sequence.fold(base, function) -> value
    sequence.fold(base, function, emit=function[, final_emit=function]) -> sequence
    
    Apply a function to a sequence in order, maintaining state via an accumulator. The `fold` command returns either a single value or a new sequence.
    
    In its first form, `fold` operates like reduce, returning a value by applying a combining function to each element in a sequence, passing the current element and the previous reduction result to the function. However, `fold` has the following differences from `reduce`:
    
    * it is guaranteed to proceed through the sequence from first element to last.
    * it passes an initial base value to the function with the first element in place of the previous reduction result.
    
    In its second form, `fold` operates like concat_map, returning a new sequence rather than a single value. When an `emit` function is provided, `fold` will:
    
    * proceed through the sequence in order and take an initial base value, as above.
    * for each element in the sequence, call both the combining function and a separate emitting function with the current element and previous reduction result.
    * optionally pass the result of the combining function to the emitting function.
    
    If provided, the emitting function must return a list.
    
    *Example* Concatenate words from a list.
    
        r.table('words').order_by('id').fold('',
            lambda acc, word: acc + r.branch(acc == '', '', ', ') + word
        ).run(conn)
    
    (This example could be implemented with `reduce`, but `fold` will preserve the order when `words` is a RethinkDB table or other stream, which is not guaranteed with `reduce`.)
    
    *Example* Return every other row in a table.
    
        r.table('even_things').fold(0,
            lambda acc, row: acc + 1,
            emit=lambda acc, row: r.branch((acc % 2 == 0), [row], [])
        ).run(conn)
    
    The first function increments the accumulator each time it's called, starting at `0`; the second function, the emitting function, alternates between returning a single-item list containing the current row or an empty list. The `fold` command will return a concatenated list of each emitted value.
    
    *Example* Compute a five-day running average for a weight tracker.
    
        r.table('tracker').filter({'name': 'bob'}).order_by('date')['weight'].fold(
            [],
            lambda acc, row: ([row] + acc).limit(5),
            emit=lambda acc, row, new_acc: r.branch(new_acc.size() == 5, [new_acc.avg()], [])
        ).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.for_each()
    '''sequence.for_each(write_function) -> object
    
    Loop over a sequence, evaluating the given write query for each element.
    
    *Example* Now that our heroes have defeated their villains, we can safely remove them from the villain table.
    
        r.table('marvel').for_each(
            lambda hero: r.table('villains').get(hero['villainDefeated']).delete()
        ).run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.ge()
    '''value.ge(value[, value, ...]) -> bool
    value >= value -> bool
    
    Compare values, testing if the left-hand value is greater or equal to than the right-hand.
    
    *Example* Test if a player has scored 10 points or more.
    
        r.table('players').get(1)['score'].ge(10).run(conn)
        # alternative syntax
        (r.table('players').get(1)['score'] >= 10).run(conn)
    
    *Example* Test if variables are ordered from lowest to highest.
    
        a = 10
        b = 20
        c = 15
        r.ge(a, b, c).run(conn)
    
    This is the equivalent of the following:
    
        r.ge(a, b).and(r.ge(b, c)).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.get_field()
    '''sequence.get_field(attr) -> sequence
    singleSelection.get_field(attr) -> value
    object.get_field(attr) -> value
    
    Get a single field from an object. If called on a sequence, gets that field from every
    object in the sequence, skipping objects that lack it.
    
    *Example* What was Iron Man's first appearance in a comic?
    
        r.table('marvel').get('IronMan').get_field('firstAppearance').run(conn)
    "'''
def rethinkdb.ast.RqlQuery.group()
    '''sequence.group(field | function..., [index=<indexname>, multi=False]) -> grouped_stream
    
    Takes a stream and partitions it into multiple groups based on the
    fields or functions provided.
    
    With the `multi` flag single documents can be assigned to multiple groups, similar to the behavior of [multi-indexes](http://rethinkdb.com/docs/secondary-indexes/python). When `multi` is `True` and the grouping value is an array, documents will be placed in each group that corresponds to the elements of the array. If the array is empty the row will be ignored.
    
    Suppose that the table `games` has the following data:
    
        [
            {"id": 2, "player": "Bob", "points": 15, "type": "ranked"},
            {"id": 5, "player": "Alice", "points": 7, "type": "free"},
            {"id": 11, "player": "Bob", "points": 10, "type": "free"},
            {"id": 12, "player": "Alice", "points": 2, "type": "free"}
        ]
    
    *Example* Group games by player.
    
        > r.table(\'games\').group(\'player\').run(conn)
        
        {
            "Alice": [
                {"id": 5, "player": "Alice", "points": 7, "type": "free"},
                {"id": 12, "player": "Alice", "points": 2, "type": "free"}
            ],
            "Bob": [
                {"id": 2, "player": "Bob", "points": 15, "type": "ranked"},
                {"id": 11, "player": "Bob", "points": 10, "type": "free"}
            ]
        }
    
    <!-- stop -->
    
    Commands chained after `group` will be called on each of these grouped
    sub-streams, producing grouped data.
    
    *Example* What is each player\'s best game?
    
        > r.table(\'games\').group(\'player\').max(\'points\').run(conn)
        
        {
            "Alice": {"id": 5, "player": "Alice", "points": 7, "type": "free"},
            "Bob": {"id": 2, "player": "Bob", "points": 15, "type": "ranked"}
        }
    
    Commands chained onto grouped data will operate on each grouped datum,
    producing more grouped data.
    
    *Example* What is the maximum number of points scored by each player?
    
        > r.table(\'games\').group(\'player\').max(\'points\')[\'points\'].run(conn)
        
        {
            "Alice": 7,
            "Bob": 15
        }
    
    You can also group by more than one field.
    
    *Example* What is the maximum number of points scored by each
    player for each game type?
    
        > r.table(\'games\').group(\'player\', \'type\').max(\'points\')[\'points\'].run(conn)
        
        {
            ("Alice", "free"): 7,
            ("Bob", "free"): 10,
            ("Bob", "ranked"): 15
        }
    
    You can also group by a function.
    
    *Example* What is the maximum number of points scored by each
    player for each game type?
    
        > r.table(\'games\')
            .group(lambda game:
                game.pluck(\'player\', \'type\')
            ).max(\'points\')[\'points\'].run(conn)
        
        {
            frozenset([(\'player\', \'Alice\'), (\'type\', \'free\')]): 7,
            frozenset([(\'player\', \'Bob\'), (\'type\', \'free\')]): 10,
            frozenset([(\'player\', \'Bob\'), (\'type\', \'ranked\')]): 15,
        }
    
    Using a function, you can also group by date on a ReQL [date field](http://rethinkdb.com/docs/dates-and-times/javascript/).
    
    *Example* How many matches have been played this year by month?
    
        > r.table(\'matches\').group(
              lambda match: [match[\'date\'].year(), match[\'date\'].month()]
          ).count().run(conn)
        
        {
            (2014, 2): 2,
            (2014, 3): 2,
            (2014, 4): 1,
            (2014, 5): 3
        }
    
    You can also group on an index (primary key or secondary).
    
    *Example* What is the maximum number of points scored by game type?
    
        > r.table(\'games\').group(index=\'type\').max(\'points\')[\'points\'].run(conn)
        
        {
            "free": 10,
            "ranked": 15
        }
    
    Suppose that the table `games2` has the following data:
    
        [
            { \'id\': 1, \'matches\': {\'a\': [1, 2, 3], \'b\': [4, 5, 6]} },
            { \'id\': 2, \'matches\': {\'b\': [100], \'c\': [7, 8, 9]} },
            { \'id\': 3, \'matches\': {\'a\': [10, 20], \'c\': [70, 80]} }
        ]
    
    Using the `multi` option we can group data by match A, B or C.
    
        > r.table(\'games2\').group(r.row[\'matches\'].keys(), multi=True).run(conn)
        
        [
            {
                \'group\': \'a\',
                \'reduction\': [ <id 1>, <id 3> ]
            },
            {
                \'group\': \'b\',
                \'reduction\': [ <id 1>, <id 2> ]
            },
            {
                \'group\': \'c\',
                \'reduction\': [ <id 2>, <id 3> ]
            }
        ]
    
    (The full result set is abbreviated in the figure; `<id 1>, <id 2>` and `<id 3>` would be the entire documents matching those keys.)
    
    *Example* Use [map](http://rethinkdb.com/api/python/map) and [sum](http://rethinkdb.com/api/python/sum) to get the total points scored for each match.
    
        r.table(\'games2\').group(r.row[\'matches\'].keys(), multi=True).ungroup().map(
            lambda doc: { \'match\': doc[\'group\'], \'total\': doc[\'reduction\'].sum(
                lambda set: set[\'matches\'][doc[\'group\']].sum()
            )}).run(conn)
        
        [
            { \'match\': \'a\', \'total\': 36 },
            { \'match\': \'b\', \'total\': 115 },
            { \'match\': \'c\', \'total\': 174 }
        ]
    
    The inner `sum` adds the scores by match within each document; the outer `sum` adds those results together for a total across all the documents.
    
    If you want to operate on all the groups rather than operating on each
    group (e.g. if you want to order the groups by their reduction), you
    can use [ungroup](http://rethinkdb.com/api/python/ungroup/) to turn a grouped stream or
    grouped data into an array of objects representing the groups.
    
    *Example* Ungrouping grouped data.
    
        > r.table(\'games\').group(\'player\').max(\'points\')[\'points\'].ungroup().run(conn)
        
        [
            {
                "group": "Alice",
                "reduction": 7
            },
            {
                "group": "Bob",
                "reduction": 15
            }
        ]
    
    Ungrouping is useful e.g. for ordering grouped data, or for inserting
    grouped data into a table.
    
    *Example* What is the maximum number of points scored by each
    player, with the highest scorers first?
    
        > r.table(\'games\').group(\'player\').max(\'points\')[\'points\'].ungroup().order_by(
                r.desc(\'reduction\')).run(conn)
        
        [
            {
                "group": "Bob",
                "reduction": 15
            },
            {
                "group": "Alice",
                "reduction": 7
            }
        ]
    
    When grouped data are returned to the client, they are transformed
    into a client-specific native type.  (Something similar is done with
    [times](http://rethinkdb.com/docs/dates-and-times/).)  In Python, grouped data are
    transformed into a `dictionary`. If the group value is an `array`, the
    key is converted to a `tuple`. If the group value is a `dictionary`,
    it will be converted to a `frozenset`.
    
    If you instead want to receive the raw
    pseudotype from the server (e.g. if you\'re planning to serialize the
    result as JSON), you can specify `group_format: \'raw\'` as an optional
    argument to `run`:
    
    *Example* Get back the raw `GROUPED_DATA` pseudotype.
    
        > r.table(\'games\').group(\'player\').avg(\'points\').run(conn, group_format=\'raw\')
        
        {
            "$reql_type$": "GROUPED_DATA",
            "data": [
                ["Alice", 4.5],
                ["Bob", 12.5]
            ]
        }
    
    Not passing the `group_format` flag would return:
    
        {
            "Alice": 4.5,
            "Bob": 12.5
        }
    
    You might also want to use the [ungroup](http://rethinkdb.com/api/python/ungroup/)
    command (see above), which will turn the grouped data into an array of
    objects on the server.
    
    If you run a query that returns a grouped stream, it will be
    automatically converted to grouped data before being sent back to you
    (there is currently no efficient way to stream groups from RethinkDB).
    This grouped data is subject to the array size limit (see [run](http://rethinkdb.com/api/python/run)).
    
    In general, operations on grouped streams will be efficiently
    distributed, and operations on grouped data won\'t be.  You can figure
    out what you\'re working with by putting `type_of` on the end of your
    query.  Below are efficient and inefficient examples.
    
    *Example* Efficient operation.
    
        # r.table(\'games\').group(\'player\').type_of().run(conn)
        # Returns "GROUPED_STREAM"
        r.table(\'games\').group(\'player\').min(\'points\').run(conn) # EFFICIENT
    
    *Example* Inefficient operation.
    
        # r.table(\'games\').group(\'player\').order_by(\'score\').type_of().run(conn)
        # Returns "GROUPED_DATA"
        r.table(\'games\').group(\'player\').order_by(\'score\').nth(0).run(conn) # INEFFICIENT
    
    What does it mean to be inefficient here?  When operating on grouped
    data rather than a grouped stream, *all* of the data has to be
    available on the node processing the query.  This means that the
    operation will only use one server\'s resources, and will require
    memory proportional to the size of the grouped data it\'s operating
    on.  (In the case of the [order_by](http://rethinkdb.com/api/python/order_by/) in the inefficient example, that
    means memory proportional **to the size of the table**.)  The array
    limit is also enforced for grouped data, so the `order_by` example
    would fail for tables with more than 100,000 rows unless you used the `array_limit` option with `run`.
    
    *Example* What is the maximum number of points scored by each
    player in free games?
    
        > r.table(\'games\').filter(lambda game:
                game[\'type\'] = \'free\'
            ).group(\'player\').max(\'points\')[\'points\'].run(conn)
        
        {
            "Alice": 7,
            "Bob": 10
        }
    
    *Example* What is each player\'s highest even and odd score?
    
        > r.table(\'games\')
            .group(\'name\', lambda game:
                game[\'points\'] % 2
            ).max(\'points\')[\'points\'].run(conn)
        
        {
            ("Alice", 1): 7,
            ("Bob", 0): 10,
            ("Bob", 1): 15
        }
    '''
def rethinkdb.ast.RqlQuery.gt()
    '''value.gt(value[, value, ...]) -> bool
    value > value -> bool
    
    Compare values, testing if the left-hand value is greater than the right-hand.
    
    *Example* Test if a player has scored more than 10 points.
    
        r.table('players').get(1)['score'].gt(10).run(conn)
        # alternative syntax
        (r.table('players').get(1)['score'] > 10).run(conn)
    
    *Example* Test if variables are ordered from lowest to highest, with no values being equal to one another.
    
        a = 10
        b = 20
        c = 15
        r.gt(a, b, c).run(conn)
    
    This is the equivalent of the following:
    
        r.gt(a, b).and(r.gt(b, c)).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.has_fields()
    '''sequence.has_fields([selector1, selector2...]) -> stream
    array.has_fields([selector1, selector2...]) -> array
    object.has_fields([selector1, selector2...]) -> boolean
    
    Test if an object has one or more fields. An object has a field if it has that key and the key has a non-null value. For instance, the object `{\'a\': 1,\'b\': 2,\'c\': null}` has the fields `a` and `b`.
    
    When applied to a single object, `has_fields` returns `true` if the object has the fields and `false` if it does not. When applied to a sequence, it will return a new sequence (an array or stream) containing the elements that have the specified fields.
    
    *Example* Return the players who have won games.
    
        r.table(\'players\').has_fields(\'games_won\').run(conn)
    
    *Example* Return the players who have *not* won games. To do this, use `has_fields` with [not](http://rethinkdb.com/api/python/not), wrapped with [filter](http://rethinkdb.com/api/python/filter).
    
        r.table(\'players\').filter(~r.row.has_fields(\'games_won\')).run(conn)
    
    *Example* Test if a specific player has won any games.
    
        r.table(\'players\').get(
            \'b5ec9714-837e-400c-aa74-dbd35c9a7c4c\').has_fields(\'games_won\').run(conn)
    
    **Nested Fields**
    
    `has_fields` lets you test for nested fields in objects. If the value of a field is itself a set of key/value pairs, you can test for the presence of specific keys.
    
    *Example* In the `players` table, the `games_won` field contains one or more fields for kinds of games won:
    
        {
            \'games_won\': {
                \'playoffs\': 2,
                \'championships\': 1
            }
        }
    
    Return players who have the "championships" field.
    
        r.table(\'players\').has_fields({\'games_won\': {\'championships\': True}}).run(conn)
    
    Note that `True` in the example above is testing for the existence of `championships` as a field, not testing to see if the value of the `championships` field is set to `true`. There\'s a more convenient shorthand form available. (See [pluck](http://rethinkdb.com/api/python/pluck) for more details on this.)
    
        r.table(\'players\').has_fields({\'games_won\': \'championships\'}).run(conn)
    '''
def rethinkdb.ast.RqlQuery.hours()
    '''time.hours() -> number
    
    Return the hour in a time object as a number between 0 and 23.
    
    *Example* Return all the posts submitted after midnight and before 4am.
    
        r.table("posts").filter(lambda post:
            post["date"].hours() < 4
        ).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.in_timezone()
    '''time.in_timezone(timezone) -> time
    
    Return a new time object with a different timezone. While the time stays the same, the results returned by methods such as hours() will change since they take the timezone into account. The timezone argument has to be of the ISO 8601 format.
    
    *Example* Hour of the day in San Francisco (UTC/GMT -8, without daylight saving time).
    
        r.now().in_timezone('-08:00').hours().run(conn)
    "'''
def rethinkdb.ast.RqlQuery.includes()
    '''sequence.includes(geometry) -> sequence
    geometry.includes(geometry) -> bool
    
    Tests whether a geometry object is completely contained within another. When applied to a sequence of geometry objects, `includes` acts as a [filter](http://rethinkdb.com/api/python/filter), returning a sequence of objects from the sequence that include the argument.
    
    *Example* Is `point2` included within a 2000-meter circle around `point1`?
    
        > point1 = r.point(-117.220406, 32.719464)
        > point2 = r.point(-117.206201, 32.725186)
        > r.circle(point1, 2000).includes(point2).run(conn)
        
        True
    
    *Example* Which of the locations in a list of parks include `circle1`?
    
        circle1 = r.circle([-117.220406, 32.719464], 10, unit='mi')
        r.table('parks')['area'].includes(circle1).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.info()
    '''any.info() -> object
    r.info(any) -> object
    
    Get information about a ReQL value.
    
    *Example* Get information about a table such as primary key, or cache size.
    
        r.table('marvel').info().run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.inner_join()
    '''sequence.inner_join(other_sequence, predicate_function) -> stream
    array.inner_join(other_sequence, predicate_function) -> array
    
    Returns an inner join of two sequences.
    
    The returned sequence represents an intersection of the left-hand sequence and the right-hand sequence: each row of the left-hand sequence will be compared with each row of the right-hand sequence to find all pairs of rows which satisfy the predicate. Each matched pair of rows of both sequences are combined into a result row. In most cases, you will want to follow the join with [zip](http://rethinkdb.com/api/python/zip) to combine the left and right results.
    
    *Example* Return a list of all matchups between Marvel and DC heroes in which the DC hero could beat the Marvel hero in a fight.
    
        r.table('marvel').inner_join(r.table('dc'),
            lambda marvel_row, dc_row: marvel_row['strength'] < dc_row['strength']
        ).zip().run(conn)
    
    <!-- stop -->
    
    (Compare this to an [outer_join](http://rethinkdb.com/api/python/outer_join) with the same inputs and predicate, which would return a list of *all* Marvel heroes along with any DC heroes with a higher strength.)"'''
def rethinkdb.ast.RqlQuery.insert_at()
    '''array.insert_at(index, value) -> array
    
    Insert a value in to an array at a given index. Returns the modified array.
    
    *Example* Hulk decides to join the avengers.
    
        r.expr(["Iron Man", "Spider-Man"]).insert_at(1, "Hulk").run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.intersects()
    '''sequence.intersects(geometry) -> sequence
    geometry.intersects(geometry) -> bool
    r.intersects(sequence, geometry) -> sequence
    r.intersects(geometry, geometry) -> bool
    
    Tests whether two geometry objects intersect with one another. When applied to a sequence of geometry objects, `intersects` acts as a [filter](http://rethinkdb.com/api/python/filter), returning a sequence of objects from the sequence that intersect with the argument.
    
    *Example* Is `point2` within a 2000-meter circle around `point1`?
    
        > point1 = r.point(-117.220406, 32.719464)
        > point2 = r.point(-117.206201, 32.725186)
        > r.circle(point1, 2000).intersects(point2).run(conn)
        
        True
    
    *Example* Which of the locations in a list of parks intersect `circle1`?
    
        circle1 = r.circle([-117.220406, 32.719464], 10, unit='mi')
        r.table('parks')('area').intersects(circle1).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.is_empty()
    '''sequence.is_empty() -> bool
    
    Test if a sequence is empty.
    
    *Example* Are there any documents in the marvel table?
    
        r.table('marvel').is_empty().run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.keys()
    '''singleSelection.keys() -> array
    object.keys() -> array
    
    Return an array containing all of an object\'s keys. Note that the keys will be sorted as described in [ReQL data types](http://rethinkdb.com/docs/data-types/#sorting-order) (for strings, lexicographically).
    
    *Example* Get all the keys from a table row.
    
        # row: { "id": 1, "mail": "fred@example.com", "name": "fred"  }
        
        r.table(\'users\').get(1).keys().run(conn)
        
        > [ "id", "mail", "name" ]
    '''
def rethinkdb.ast.RqlQuery.le()
    '''value.le(value[, value, ...]) -> bool
    value <= value -> bool
    
    Compare values, testing if the left-hand value is less than or equal to the right-hand.
    
    *Example* Test if a player has scored 10 points or less.
    
        r.table('players').get(1)['score'].le(10).run(conn)
        # alternative syntax
        (r.table('players').get(1)['score'] <= 10).run(conn)
    
    *Example* Test if variables are ordered from highest to lowest.
    
        a = 20
        b = 10
        c = 15
        r.le(a, b, c).run(conn)
    
    This is the equivalent of the following:
    
        r.le(a, b).and(r.le(b, c)).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.limit()
    '''sequence.limit(n) -> stream
    array.limit(n) -> array
    
    End the sequence after the given number of elements.
    
    *Example* Only so many can fit in our Pantheon of heroes.
    
        r.table('marvel').order_by('belovedness').limit(10).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.lt()
    '''value.lt(value[, value, ...]) -> bool
    value < value -> bool
    
    Compare values, testing if the left-hand value is less than the right-hand.
    
    *Example* Test if a player has scored less than 10 points.
    
        r.table('players').get(1)['score'].lt(10).run(conn)
        # alternative syntax
        (r.table('players').get(1)['score'] < 10).run(conn)
    
    *Example* Test if variables are ordered from highest to lowest, with no values being equal to one another.
    
        a = 20
        b = 10
        c = 15
        r.lt(a, b, c).run(conn)
    
    This is the equivalent of the following:
    
        r.lt(a, b).and(r.lt(b, c)).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.map()
    '''sequence1.map([sequence2, ...], function) -> stream
    array1.map([array2, ...], function) -> array
    r.map(sequence1[, sequence2, ...], function) -> stream
    r.map(array1[, array2, ...], function) -> array
    
    Transform each element of one or more sequences by applying a mapping function to them. If `map` is run with two or more sequences, it will iterate for as many items as there are in the shortest sequence.
    
    Note that `map` can only be applied to sequences, not single values. If you wish to apply a function to a single value/selection (including an array), use the [do](http://rethinkdb.com/api/python/do) command.
    
    *Example* Return the first five squares.
    
        > r.expr([1, 2, 3, 4, 5]).map(lambda val: (val * val)).run(conn)
        
        [1, 4, 9, 16, 25]
    
    *Example* Sum the elements of three sequences.
    
        > sequence1 = [100, 200, 300, 400]
        > sequence2 = [10, 20, 30, 40]
        > sequence3 = [1, 2, 3, 4]
        > r.map(sequence1, sequence2, sequence3,
            lambda val1, val2, val3: (val1 + val2 + val3)).run(conn)
        
        [111, 222, 333, 444]
    
    *Example* Rename a field when retrieving documents using `map` and [merge](http://rethinkdb.com/api/python/merge/).
    
    This example renames the field `id` to `user_id` when retrieving documents from the table `users`.
    
        r.table('users').map(
            lambda doc: doc.merge({'user_id': doc['id']}).without('id')).run(conn)
    
    Note that in this case, [row](http://rethinkdb.com/api/python/row) may be used as an alternative to writing an anonymous function, as it returns the same value as the function parameter receives:
    
        r.table('users').map(
            r.row.merge({'user_id': r.row['id']}).without('id')).run(conn)
    
    *Example* Assign every superhero an archenemy.
    
        r.table('heroes').map(r.table('villains'),
            lambda hero, villain: hero.merge({'villain': villain})).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.match()
    '''string.match(regexp) -> None/object
    
    Matches against a regular expression. If there is a match, returns an object with the fields:
    
    - `str`: The matched string
    - `start`: The matched string\'s start
    - `end`: The matched string\'s end
    - `groups`: The capture groups defined with parentheses
    
    If no match is found, returns `None`.
    
    <!-- break -->
    
    Accepts RE2 syntax
    ([https://code.google.com/p/re2/wiki/Syntax](https://code.google.com/p/re2/wiki/Syntax)).
    You can enable case-insensitive matching by prefixing the regular expression with
    `(?i)`. See the linked RE2 documentation for more flags.
    
    The `match` command does not support backreferences.
    
    *Example* Get all users whose name starts with "A". Because `None` evaluates to `false` in
    [filter](http://rethinkdb.com/api/python/filter/), you can just use the result of `match` for the predicate.
    
        r.table(\'users\').filter(lambda doc:
            doc[\'name\'].match("^A")
        ).run(conn)
    
    *Example* Get all users whose name ends with "n".
    
        r.table(\'users\').filter(lambda doc:
            doc[\'name\'].match("n$")
        ).run(conn)
    
    *Example* Get all users whose name has "li" in it
    
        r.table(\'users\').filter(lambda doc:
            doc[\'name\'].match("li")
        ).run(conn)
    
    *Example* Get all users whose name is "John" with a case-insensitive search.
    
        r.table(\'users\').filter(lambda doc:
            doc[\'name\'].match("(?i)^john$")
        ).run(conn)
    
    *Example* Get all users whose name is composed of only characters between "a" and "z".
    
        r.table(\'users\').filter(lambda doc:
            doc[\'name\'].match("(?i)^[a-z]+$")
        ).run(conn)
    
    *Example* Get all users where the zipcode is a string of 5 digits.
    
        r.table(\'users\').filter(lambda doc:
            doc[\'zipcode\'].match("\\d{5}")
        ).run(conn)
    
    *Example* Retrieve the domain of a basic email
    
        r.expr("name@domain.com").match(".*@(.*)").run(conn)
    
    Result:
    
        {
            "start": 0,
            "end": 20,
            "str": "name@domain.com",
            "groups":[
                {
                    "end": 17,
                    "start": 7,
                    "str": "domain.com"
                }
            ]
        }
    
    You can then retrieve only the domain with the [\\[\\]](http://rethinkdb.com/api/python/get_field) selector.
    
        r.expr("name@domain.com").match(".*@(.*)")["groups"][0]["str"].run(conn)
    
    Returns `\'domain.com\'`
    
    *Example* Fail to parse out the domain and returns `None`.
    
        r.expr("name[at]domain.com").match(".*@(.*)").run(conn)
    '''
def rethinkdb.ast.RqlQuery.max()
    '''sequence.max(field | function) -> element
    sequence.max(index=<indexname>) -> element
    
    Finds the maximum element of a sequence.
    
    The `max` command can be called with:
    
    * a **field name**, to return the element of the sequence with the largest value in that field;
    * an **index** (the primary key or a secondary index), to return the element of the sequence with the largest value in that index;
    * a **function**, to apply the function to every element within the sequence and return the element which returns the largest value from the function, ignoring any elements where the function produces a non-existence error.
    
    For more information on RethinkDB's sorting order, read the section in [ReQL data types](http://rethinkdb.com/docs/data-types/#sorting-order).
    
    Calling `max` on an empty sequence will throw a non-existence error; this can be handled using the [default](http://rethinkdb.com/api/python/default/) command.
    
    *Example* Return the maximum value in the list `[3, 5, 7]`.
    
        r.expr([3, 5, 7]).max().run(conn)
    
    *Example* Return the user who has scored the most points.
    
        r.table('users').max('points').run(conn)
    
    *Example* The same as above, but using a secondary index on the `points` field.
    
        r.table('users').max(index='points').run(conn)
    
    *Example* Return the user who has scored the most points, adding in bonus points from a separate field using a function.
    
        r.table('users').max(lambda user:
            user['points'] + user['bonus_points']
        ).run(conn)
    
    *Example* Return the highest number of points any user has ever scored. This returns the value of that `points` field, not a document.
    
        r.table('users').max('points')['points'].run(conn)
    
    *Example* Return the user who has scored the most points, but add a default `None` return value to prevent an error if no user has ever scored points.
    
        r.table('users').max('points').default(None).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.merge()
    '''singleSelection.merge([object | function, object | function, ...]) -> object
    object.merge([object | function, object | function, ...]) -> object
    sequence.merge([object | function, object | function, ...]) -> stream
    array.merge([object | function, object | function, ...]) -> array
    
    Merge two or more objects together to construct a new object with properties from all. When there is a conflict between field names, preference is given to fields in the rightmost object in the argument list `merge` also accepts a subquery function that returns an object, which will be used similarly to a [map](http://rethinkdb.com/api/python/map/) function.
    
    *Example* Equip Thor for battle.
    
        r.table(\'marvel\').get(\'thor\').merge(
            r.table(\'equipment\').get(\'hammer\'),
            r.table(\'equipment\').get(\'pimento_sandwich\')
        ).run(conn)
    
    *Example* Equip every hero for battle, using a subquery function to retrieve their weapons.
    
        r.table(\'marvel\').merge(lambda hero:
            { \'weapons\': r.table(\'weapons\').get(hero[\'weapon_id\']) }
        ).run(conn)
    
    *Example* Use `merge` to join each blog post with its comments.
    
    Note that the sequence being merged&mdash;in this example, the comments&mdash;must be coerced from a selection to an array. Without `coerce_to` the operation will throw an error ("Expected type DATUM but found SELECTION").
    
        r.table(\'posts\').merge(lambda post:
            { \'comments\': r.table(\'comments\').get_all(post[\'id\'],
                index=\'post_id\').coerce_to(\'array\') }
        ).run(conn)
    
    *Example* Merge can be used recursively to modify object within objects.
    
        r.expr({\'weapons\' : {\'spectacular graviton beam\' : {\'dmg\' : 10, \'cooldown\' : 20}}}).merge(
            {\'weapons\' : {\'spectacular graviton beam\' : {\'dmg\' : 10}}}
        ).run(conn)
    
    *Example* To replace a nested object with another object you can use the literal keyword.
    
        r.expr({\'weapons\' : {\'spectacular graviton beam\' : {\'dmg\' : 10, \'cooldown\' : 20}}}).merge(
            {\'weapons\' : r.literal({\'repulsor rays\' : {\'dmg\' : 3, \'cooldown\' : 0}})}
        ).run(conn)
    
    *Example* Literal can be used to remove keys from an object as well.
    
        r.expr({\'weapons\' : {\'spectacular graviton beam\' : {\'dmg\' : 10, \'cooldown\' : 20}}}).merge(
            {\'weapons\' : {\'spectacular graviton beam\' : r.literal()}}
        ).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.min()
    '''sequence.min(field | function) -> element
    sequence.min(index=<indexname>) -> element
    
    Finds the minimum element of a sequence.
    
    The `min` command can be called with:
    
    * a **field name**, to return the element of the sequence with the smallest value in that field;
    * an **index** (the primary key or a secondary index), to return the element of the sequence with the smallest value in that index;
    * a **function**, to apply the function to every element within the sequence and return the element which returns the smallest value from the function, ignoring any elements where the function produces a non-existence error.
    
    For more information on RethinkDB's sorting order, read the section in [ReQL data types](http://rethinkdb.com/docs/data-types/#sorting-order).
    
    Calling `min` on an empty sequence will throw a non-existence error; this can be handled using the [default](http://rethinkdb.com/api/python/default/) command.
    
    *Example* Return the minimum value in the list `[3, 5, 7]`.
    
        r.expr([3, 5, 7]).min().run(conn)
    
    *Example* Return the user who has scored the fewest points.
    
        r.table('users').min('points').run(conn)
    
    *Example* The same as above, but using a secondary index on the `points` field.
    
        r.table('users').min(index='points').run(conn)
    
    *Example* Return the user who has scored the fewest points, adding in bonus points from a separate field using a function.
    
        r.table('users').min(lambda user:
            user['points'] + user['bonus_points']
        ).run(conn)
    
    *Example* Return the smallest number of points any user has ever scored. This returns the value of that `points` field, not a document.
    
        r.table('users').min('points')['points'].run(conn)
    
    *Example* Return the user who has scored the fewest points, but add a default `None` return value to prevent an error if no user has ever scored points.
    
        r.table('users').min('points').default(None).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.minutes()
    '''time.minutes() -> number
    
    Return the minute in a time object as a number between 0 and 59.
    
    *Example* Return all the posts submitted during the first 10 minutes of every hour.
    
        r.table("posts").filter(lambda post:
            post["date"].minutes() < 10
        ).run(conn)
    '''
def rethinkdb.ast.RqlQuery.month()
    '''time.month() -> number
    
    Return the month of a time object as a number between 1 and 12. For your convenience, the terms r.january, r.february etc. are defined and map to the appropriate integer.
    
    *Example* Retrieve all the users who were born in November.
    
        r.table("users").filter(
            r.row["birthdate"].month() == 11
        )
    
    *Example* Retrieve all the users who were born in November.
    
        r.table("users").filter(
            r.row["birthdate"].month() == r.november
        )
    
    '''
def rethinkdb.ast.RqlQuery.ne()
    '''value.ne(value[, value, ...]) -> bool
    value != value -> bool
    
    Test if two or more values are not equal.
    
    *Example* See if a user's `role` field is not set to `administrator`. 
    
        r.table('users').get(1)['role'].ne('administrator').run(conn)
        # alternative syntax
        (r.table('users').get(1)['role'] != 'administrator').run(conn)
    
    *Example* See if three variables do not contain equal values.
    
        r.ne(a, b, c).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.not_()
    '''bool.not_() -> bool
    not_(bool) -> bool
    (~bool) -> bool
    
    Compute the logical inverse (not) of an expression.
    
    `not_` can be called either via method chaining, immediately after an expression that evaluates as a boolean value, or by passing the expression as a parameter to `not_`.  All values that are not `False` or `None` will be converted to `True`.
    
    You may also use `~` as a shorthand operator.
    
    *Example* Not true is false.
    
        r.not_(True).run(conn)
        r.expr(True).not_().run(conn)
        (~r.expr(True)).run(conn)
    
    These evaluate to `false`.
    
    Note that when using `~` the expression is wrapped in parentheses. Without this, Python will evaluate `r.expr(True)` *first* rather than using the ReQL operator and return an incorrect value. (`~True` evaluates to &minus;2 in Python.)
    
    *Example* Return all the users that do not have a "flag" field.
    
        r.table(\'users\').filter(
            lambda users: (~users.has_fields(\'flag\'))
        ).run(conn)
    
    *Example* As above, but prefix-style.
    
        r.table(\'users\').filter(
            lambda users: r.not_(users.has_fields(\'flag\'))
        ).run(conn)
    '''
def rethinkdb.ast.RqlQuery.nth()
    '''sequence.nth(index) -> object
    selection.nth(index) -> selection&lt;object&gt;
    
    Get the *nth* element of a sequence, counting from zero. If the argument is negative, count from the last element.
    
    *Example* Select the second element in the array.
    
        r.expr([1,2,3]).nth(1).run(conn)
        r.expr([1,2,3])[1].run(conn)
    
    *Example* Select the bronze medalist from the competitors.
    
        r.table('players').order_by(index=r.desc('score')).nth(3).run(conn)
    
    *Example* Select the last place competitor.
    
        r.table('players').order_by(index=r.desc('score')).nth(-1).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.offsets_of()
    '''sequence.offsets_of(datum | predicate_function) -> array
    
    Get the indexes of an element in a sequence. If the argument is a predicate, get the indexes of all elements matching it.
    
    *Example* Find the position of the letter 'c'.
    
        r.expr(['a','b','c']).offsets_of('c').run(conn)
    
    *Example* Find the popularity ranking of invisible heroes.
    
        r.table('marvel').union(r.table('dc')).order_by('popularity').offsets_of(
            r.row['superpowers'].contains('invisibility')
        ).run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.outer_join()
    '''sequence.outer_join(other_sequence, predicate_function) -> stream
    array.outer_join(other_sequence, predicate_function) -> array
    
    Returns a left outer join of two sequences. The returned sequence represents a union of the left-hand sequence and the right-hand sequence: all documents in the left-hand sequence will be returned, each matched with a document in the right-hand sequence if one satisfies the predicate condition. In most cases, you will want to follow the join with [zip](http://rethinkdb.com/api/python/zip) to combine the left and right results.
    
    *Example* Return a list of all Marvel heroes, paired with any DC heroes who could beat them in a fight.
    
        r.table('marvel').outer_join(r.table('dc'),
          lambda marvel_row, dc_row: marvel_row['strength'] < dc_row['strength']
        ).zip().run(conn)
    
    (Compare this to an [inner_join](http://rethinkdb.com/api/python/inner_join) with the same inputs and predicate, which would return a list only of the matchups in which the DC hero has the higher strength.)
    "'''
def rethinkdb.ast.RqlQuery.pluck()
    '''sequence.pluck([selector1, selector2...]) -> stream
    array.pluck([selector1, selector2...]) -> array
    object.pluck([selector1, selector2...]) -> object
    singleSelection.pluck([selector1, selector2...]) -> object
    
    Plucks out one or more attributes from either an object or a sequence of objects
    (projection).
    
    *Example* We just need information about IronMan's reactor and not the rest of the
    document.
    
        r.table('marvel').get('IronMan').pluck('reactorState', 'reactorPower').run(conn)
    
    *Example* For the hero beauty contest we only care about certain qualities.
    
        r.table('marvel').pluck('beauty', 'muscleTone', 'charm').run(conn)
    
    *Example* Pluck can also be used on nested objects.
    
        r.table('marvel').pluck({'abilities' : {'damage' : True, 'mana_cost' : True}, 'weapons' : True}).run(conn)
    
    *Example* The nested syntax can quickly become overly verbose so there's a shorthand
    for it.
    
        r.table('marvel').pluck({'abilities' : ['damage', 'mana_cost']}, 'weapons').run(conn)
    
    For more information read the [nested field documentation](http://rethinkdb.com/docs/nested-fields/).
    "'''
def rethinkdb.ast.RqlQuery.polygon_sub()
    '''polygon1.polygon_sub(polygon2) -> polygon
    
    Use `polygon2` to "punch out" a hole in `polygon1`. `polygon2` must be completely contained within `polygon1` and must have no holes itself (it must not be the output of `polygon_sub` itself).
    
    *Example* Define a polygon with a hole punched in it.
    
        outer_polygon = r.polygon(
            [-122.4, 37.7],
            [-122.4, 37.3],
            [-121.8, 37.3],
            [-121.8, 37.7]
        )
        inner_polygon = r.polygon(
            [-122.3, 37.4],
            [-122.3, 37.6],
            [-122.0, 37.6],
            [-122.0, 37.4]
        )
        outer_polygon.polygon_sub(inner_polygon).run(conn)
    '''
def rethinkdb.ast.RqlQuery.prepend()
    '''array.prepend(value) -> array
    
    Prepend a value to an array.
    
    *Example* Retrieve Iron Man's equipment list with the addition of some new boots.
    
        r.table('marvel').get('IronMan')['equipment'].prepend('newBoots').run(conn)
    "'''
def rethinkdb.ast.RqlQuery.reduce()
    '''sequence.reduce(function) -> value
    
    Produce a single value from a sequence through repeated application of a reduction function.
    
    The reduction function can be called on:
    
    - two elements of the sequence
    - one element of the sequence and one result of a previous reduction
    - two results of previous reductions
    
    The reduction function can be called on the results of two previous reductions because the
    `reduce` command is distributed and parallelized across shards and CPU cores. A common
    mistaken when using the `reduce` command is to suppose that the reduction is executed
    from left to right. Read the [map-reduce in RethinkDB](http://rethinkdb.com/docs/map-reduce/) article to
    see an example.
    
    If the sequence is empty, the server will produce a `ReqlRuntimeError` that can be
    caught with `default`.  
    If the sequence has only one element, the first element will be returned.
    
    *Example* Return the number of documents in the table `posts`.
    
        r.table("posts").map(lambda doc: 1)
            .reduce(lambda left, right: left+right)
            .default(0).run(conn)
    
    A shorter way to execute this query is to use [count](http://rethinkdb.com/api/python/count).
    
    *Example* Suppose that each `post` has a field `comments` that is an array of
    comments.  
    Return the number of comments for all posts.
    
        r.table("posts").map(lambda doc:
            doc["comments"].count()
        ).reduce(lambda left, right:
            left+right
        ).default(0).run(conn)
    
    *Example* Suppose that each `post` has a field `comments` that is an array of
    comments.  
    Return the maximum number comments per post.
    
        r.table("posts").map(lambda doc:
            doc["comments"].count()
        ).reduce(lambda left, right:
            r.branch(
                left > right,
                left,
                right
            )
        ).default(0).run(conn)
    
    A shorter way to execute this query is to use [max](http://rethinkdb.com/api/python/max).
    '''
def rethinkdb.ast.RqlQuery.round()
    '''r.round(number) -> number
    number.round() -> number
    
    Rounds the given value to the nearest whole integer.
    
    For example, values of 1.0 up to but not including 1.5 will return 1.0, similar to floor; values of 1.5 up to 2.0 will return 2.0, similar to ceil.
    
    *Example* Round 12.345 to the nearest integer.
    
        > r.round(12.345).run(conn)
        
        12.0
    
    The `round` command can also be chained after an expression.
    
    *Example* Round -12.345 to the nearest integer.
    
        > r.expr(-12.345).round().run(conn)
        
        -12.0
    
    *Example* Return Iron Man's weight, rounded to the nearest integer.
    
        r.table('superheroes').get('ironman')['weight'].round().run(conn)
    "'''
def rethinkdb.ast.RqlQuery.run()
    '''query.run(conn[, options]) -> cursor
    query.run(conn[, options]) -> object
    
    Run a query on a connection, returning either a single JSON result or
    a cursor, depending on the query.
    
    The optional arguments are:
    
    - `read_mode`: One of three possible values affecting the consistency guarantee for the query (default: `\'single\'`).
        - `\'single\'` (the default) returns values that are in memory (but not necessarily written to disk) on the primary replica.
        - `\'majority\'` will only return values that are safely committed on disk on a majority of replicas. This requires sending a message to every replica on each read, so it is the slowest but most consistent.
        - `\'outdated\'` will return values that are in memory on an arbitrarily-selected replica. This is the fastest but least consistent.
    - `time_format`: what format to return times in (default: `\'native\'`).
      Set this to `\'raw\'` if you want times returned as JSON objects for exporting.
    - `profile`: whether or not to return a profile of the query\'s
      execution (default: `False`).
    - `durability`: possible values are `\'hard\'` and `\'soft\'`. In soft durability mode RethinkDB
    will acknowledge the write immediately after receiving it, but before the write has
    been committed to disk.
    - `group_format`: what format to return `grouped_data` and `grouped_streams` in (default: `\'native\'`).
      Set this to `\'raw\'` if you want the raw pseudotype.
    - `noreply`: set to `True` to not receive the result object or cursor and return immediately.
    - `db`: the database to run this query against as a string. The default is the database specified in the `db` parameter to [connect](http://rethinkdb.com/api/python/connect/) (which defaults to `test`). The database may also be specified with the [db](http://rethinkdb.com/api/python/db/) command.
    - `array_limit`: the maximum numbers of array elements that can be returned by a query (default: 100,000). This affects all ReQL commands that return arrays. Note that it has no effect on the size of arrays being _written_ to the database; those always have an upper limit of 100,000 elements.
    - `binary_format`: what format to return binary data in (default: `\'native\'`). Set this to `\'raw\'` if you want the raw pseudotype.
    - `min_batch_rows`: minimum number of rows to wait for before batching a result set (default: 8). This is an integer.
    - `max_batch_rows`: maximum number of rows to wait for before batching a result set (default: unlimited). This is an integer.
    - `max_batch_bytes`: maximum number of bytes to wait for before batching a result set (default: 1MB). This is an integer.
    - `max_batch_seconds`: maximum number of seconds to wait before batching a result set (default: 0.5). This is a float (not an integer) and may be specified to the microsecond.
    - `first_batch_scaledown_factor`: factor to scale the other parameters down by on the first batch (default: 4). For example, with this set to 8 and `max_batch_rows` set to 80, on the first batch `max_batch_rows` will be adjusted to 10 (80 / 8). This allows the first batch to return faster.
    
    *Example* Run a query on the connection `conn` and print out every
    row in the result.
    
        for doc in r.table(\'marvel\').run(conn):
            print doc
    
    *Example* If you are OK with potentially out of date data from all
    the tables involved in this query and want potentially faster reads,
    pass a flag allowing out of date data in an options object. Settings
    for individual tables will supercede this global setting for all
    tables in the query.
    
        r.table(\'marvel\').run(conn, read_mode=\'outdated\')
    
    *Example* If you just want to send a write and forget about it, you
    can set `noreply` to true in the options. In this case `run` will
    return immediately.
    
        r.table(\'marvel\').run(conn, noreply=True)
    
    *Example* If you want to specify whether to wait for a write to be
    written to disk (overriding the table\'s default settings), you can set
    `durability` to `\'hard\'` or `\'soft\'` in the options.
    
        r.table(\'marvel\')
            .insert({ \'superhero\': \'Iron Man\', \'superpower\': \'Arc Reactor\' })
            .run(conn, noreply=True, durability=\'soft\')
    
    *Example* If you do not want a time object to be converted to a
    native date object, you can pass a `time_format` flag to prevent it
    (valid flags are "raw" and "native"). This query returns an object
    with two fields (`epoch_time` and `$reql_type$`) instead of a native date
    object.
    
        r.now().run(conn, time_format="raw")
    
    *Example* Specify the database to use for the query.
    
        for doc in r.table(\'marvel\').run(conn, db=\'heroes\'):
            print doc
    
    This is equivalent to using the `db` command to specify the database:
    
        r.db(\'heroes\').table(\'marvel\').run(conn) ...
    
    *Example* Change the batching parameters for this query.
    
        r.table(\'marvel\').run(conn, max_batch_rows=16, max_batch_bytes=2048)
    '''
def rethinkdb.ast.RqlQuery.sample()
    '''sequence.sample(number) -> selection
    stream.sample(number) -> array
    array.sample(number) -> array
    
    Select a given number of elements from a sequence with uniform random distribution. Selection is done without replacement.
    
    If the sequence has less than the requested number of elements (i.e., calling `sample(10)` on a sequence with only five elements), `sample` will return the entire sequence in a random order.
    
    *Example* Select 3 random heroes.
    
        r.table('marvel').sample(3).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.seconds()
    '''time.seconds() -> number
    
    Return the seconds in a time object as a number between 0 and 59.999 (double precision).
    
    *Example* Return the post submitted during the first 30 seconds of every minute.
    
        r.table("posts").filter(lambda post:
            post["date"].seconds() < 30
        ).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.set_difference()
    '''array.set_difference(array) -> array
    
    Remove the elements of one array from another and return them as a set (an array with
    distinct values).
    
    *Example* Check which pieces of equipment Iron Man has, excluding a fixed list.
    
        r.table('marvel').get('IronMan')['equipment'].set_difference(['newBoots', 'arc_reactor']).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.set_insert()
    '''array.set_insert(value) -> array
    
    Add a value to an array and return it as a set (an array with distinct values).
    
    *Example* Retrieve Iron Man's equipment list with the addition of some new boots.
    
        r.table('marvel').get('IronMan')['equipment'].set_insert('newBoots').run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.set_intersection()
    '''array.set_intersection(array) -> array
    
    Intersect two arrays returning values that occur in both of them as a set (an array with
    distinct values).
    
    *Example* Check which pieces of equipment Iron Man has from a fixed list.
    
        r.table('marvel').get('IronMan')['equipment'].set_intersection(['newBoots', 'arc_reactor']).run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.set_union()
    '''array.set_union(array) -> array
    
    Add a several values to an array and return it as a set (an array with distinct values).
    
    *Example* Retrieve Iron Man's equipment list with the addition of some new boots and an arc reactor.
    
        r.table('marvel').get('IronMan')['equipment'].set_union(['newBoots', 'arc_reactor']).run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.skip()
    '''sequence.skip(n) -> stream
    array.skip(n) -> array
    
    Skip a number of elements from the head of the sequence.
    
    *Example* Here in conjunction with [order_by](http://rethinkdb.com/api/python/order_by/) we choose to ignore the most successful heroes.
    
        r.table('marvel').order_by('successMetric').skip(10).run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.slice()
    '''selection.slice(start_index[, end_index, left_bound=\'closed\', right_bound=\'open\']) -> selection
    stream.slice(start_index[, end_index, left_bound=\'closed\', right_bound=\'open\']) -> stream
    array.slice(start_index[, end_index, left_bound=\'closed\', right_bound=\'open\']) -> array
    binary.slice(start_index[, end_index, left_bound=\'closed\', right_bound=\'open\']) -> binary
    string.slice(start_index[, end_index, left_bound=\'closed\', right_bound=\'open\']) -> string
    
    Return the elements of a sequence within the specified range.
    
    `slice` returns the range between `start_index` and `end_index`. If only `start_index` is specified, `slice` returns the range from that index to the end of the sequence. Specify `left_bound` or `right_bound` as `open` or `closed` to indicate whether to include that endpoint of the range by default: `closed` returns that endpoint, while `open` does not. By default, `left_bound` is closed and `right_bound` is open, so the range `(10,13)` will return the tenth, eleventh and twelfth elements in the sequence.
    
    If `end_index` is past the end of the sequence, all elements from `start_index` to the end of the sequence will be returned. If `start_index` is past the end of the sequence or `end_index` is less than `start_index`, a zero-element sequence will be returned.
    
    Negative `start_index` and `end_index` values are allowed with arrays; in that case, the returned range counts back from the array\'s end. That is, the range `(-2)` returns the last two elements, and the range of `(2,-1)` returns the second element through the next-to-last element of the range. An error will be raised on a negative `start_index` or `end_index` with non-arrays. (An `end_index` of &minus;1 *is* allowed with a stream if `right_bound` is closed; this behaves as if no `end_index` was specified.)
    
    If `slice` is used with a [binary](http://rethinkdb.com/api/python/binary) object, the indexes refer to byte positions within the object. That is, the range `(10,20)` will refer to the 10th byte through the 19th byte.
    
    With a string, `slice` behaves similarly, with the indexes referring to Unicode codepoints. String indexes start at `0`. (Note that combining codepoints are counted separately.)
    
    If you are only specifying the indexes and not the bounding options, you may use Python\'s slice operator as a shorthand: `[start_index:end_index]`.
    
    *Example* Return the fourth, fifth and sixth youngest players. (The youngest player is at index 0, so those are elements 3&ndash;5.)
    
        r.table(\'players\').order_by(index=\'age\').slice(3,6).run(conn)
    
    Or, using Python\'s slice operator:
    
        r.table(\'players\').filter({\'class\': \'amateur\'})[10:20].run(conn)
    
    *Example* Return all but the top three players who have a red flag.
    
        r.table(\'players\').filter({\'flag\': \'red\'}).order_by(index=r.desc(\'score\')).slice(3).run(conn)
    
    *Example* Return holders of tickets `X` through `Y`, assuming tickets are numbered sequentially. We want to include ticket `Y`.
    
        r.table(\'users\').order_by(index=\'ticket\').slice(x, y, right_bound=\'closed\').run(conn)
    
    *Example* Return the elements of an array from the second through two from the end (that is, not including the last two).
    
        r.expr([0,1,2,3,4,5]).slice(2,-2).run(conn)
        [2,3]
    
    *Example* Return the third through fifth characters of a string.
    
        > r.expr("rutabaga").slice(2,5).run(conn)
        "tab"
    '''
def rethinkdb.ast.RqlQuery.splice_at()
    '''array.splice_at(index, array) -> array
    
    Insert several values in to an array at a given index. Returns the modified array.
    
    *Example* Hulk and Thor decide to join the avengers.
    
        r.expr(["Iron Man", "Spider-Man"]).splice_at(1, ["Hulk", "Thor"]).run(conn)
    '''
def rethinkdb.ast.RqlQuery.split()
    '''string.split([separator, [max_splits]]) -> array
    
    Splits a string into substrings.  Splits on whitespace when called
    with no arguments.  When called with a separator, splits on that
    separator.  When called with a separator and a maximum number of
    splits, splits on that separator at most `max_splits` times.  (Can be
    called with `None` as the separator if you want to split on whitespace
    while still specifying `max_splits`.)
    
    Mimics the behavior of Python\'s `string.split` in edge cases, except
    for splitting on the empty string, which instead produces an array of
    single-character strings.
    
    *Example* Split on whitespace.
    
        > r.expr("foo  bar bax").split().run(conn)
        ["foo", "bar", "bax"]
    
    *Example* Split the entries in a CSV file.
    
        > r.expr("12,37,,22,").split(",").run(conn)
        ["12", "37", "", "22", ""]
    
    *Example* Split a string into characters.
    
        > r.expr("mlucy").split("").run(conn)
        ["m", "l", "u", "c", "y"]
    
    *Example* Split the entries in a CSV file, but only at most 3
    times.
    
        > r.expr("12,37,,22,").split(",", 3).run(conn)
        ["12", "37", "", "22,"]
    
    *Example* Split on whitespace at most once (i.e. get the first word).
    
        > r.expr("foo  bar bax").split(None, 1).run(conn)
        ["foo", "bar bax"]
    '''
def rethinkdb.ast.RqlQuery.sum()
    '''sequence.sum([field | function]) -> number
    
    Sums all the elements of a sequence.  If called with a field name,
    sums all the values of that field in the sequence, skipping elements
    of the sequence that lack that field.  If called with a function,
    calls that function on every element of the sequence and sums the
    results, skipping elements of the sequence where that function returns
    `None` or a non-existence error.
    
    Returns `0` when called on an empty sequence.
    
    *Example* What's 3 + 5 + 7?
    
        r.expr([3, 5, 7]).sum().run(conn)
    
    *Example* How many points have been scored across all games?
    
        r.table('games').sum('points').run(conn)
    
    *Example* How many points have been scored across all games,
    counting bonus points?
    
        r.table('games').sum(lambda game:
            game['points'] + game['bonus_points']
        ).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.time_of_day()
    '''time.time_of_day() -> number
    
    Return the number of seconds elapsed since the beginning of the day stored in the time object.
    
    *Example* Retrieve posts that were submitted before noon.
    
        r.table("posts").filter(
            r.row["date"].time_of_day() <= 12*60*60
        ).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.timezone()
    '''time.timezone() -> string
    
    Return the timezone of the time object.
    
    *Example* Return all the users in the "-07:00" timezone.
    
        r.table("users").filter(lambda user:
            user["subscriptionDate"].timezone() == "-07:00"
        )
    
    '''
def rethinkdb.ast.RqlQuery.to_epoch_time()
    '''time.to_epoch_time() -> number
    
    Convert a time object to its epoch time.
    
    *Example* Return the current time in seconds since the Unix Epoch with millisecond-precision.
    
        r.now().to_epoch_time()
    
    '''
def rethinkdb.ast.RqlQuery.to_geojson()
    '''geometry.to_geojson() -> object
    
    Convert a ReQL geometry object to a [GeoJSON](http://geojson.org) object.
    
    *Example* Convert a ReQL geometry object to a GeoJSON object.
    
        > r.table('geo').get('sfo')['location'].to_geojson().run(conn)
        
        {
            'type': 'Point',
            'coordinates': [ -122.423246, 37.779388 ]
        }
    "'''
def rethinkdb.ast.RqlQuery.to_iso8601()
    '''time.to_iso8601() -> string
    
    Convert a time object to a string in ISO 8601 format.
    
    *Example* Return the current ISO 8601 time.
    
        > r.now().to_iso8601().run(conn)
        
        "2015-04-20T18:37:52.690+00:00"
    
    '''
def rethinkdb.ast.RqlQuery.to_json()
    '''value.to_json_string() -> string
    value.to_json() -> string
    
    Convert a ReQL value or object to a JSON string. You may use either `to_json_string` or `to_json`.
    
    *Example* Get a ReQL document as a JSON string.
    
        > r.table(\'hero\').get(1).to_json()
        
        \'{"id": 1, "name": "Batman", "city": "Gotham", "powers": ["martial arts", "cinematic entrances"]}\'
    '''
def rethinkdb.ast.RqlQuery.to_json_string()
    '''value.to_json_string() -> string
    value.to_json() -> string
    
    Convert a ReQL value or object to a JSON string. You may use either `to_json_string` or `to_json`.
    
    *Example* Get a ReQL document as a JSON string.
    
        > r.table(\'hero\').get(1).to_json()
        
        \'{"id": 1, "name": "Batman", "city": "Gotham", "powers": ["martial arts", "cinematic entrances"]}\'
    '''
def rethinkdb.ast.RqlQuery.type_of()
    '''any.type_of() -> string
    
    Gets the type of a ReQL query\'s return value.
    
    The type will be returned as a string:
    
    * `ARRAY`
    * `BOOL`
    * `DB`
    * `FUNCTION`
    * `GROUPED_DATA`
    * `GROUPED_STREAM`
    * `MAXVAL`
    * `MINVAL`
    * `NULL`
    * `NUMBER`
    * `OBJECT`
    * `PTYPE<BINARY>`
    * `PTYPE<GEOMETRY>`
    * `PTYPE<TIME>`
    * `SELECTION<ARRAY>`
    * `SELECTION<OBJECT>`
    * `SELECTION<STREAM>`
    * `STREAM`
    * `STRING`
    * `TABLE_SLICE`
    * `TABLE`
    
    Read the article on [ReQL data types](docs/data-types/) for a more detailed discussion. Note that some possible return values from `type_of` are internal values, such as `MAXVAL`, and unlikely to be returned from queries in standard practice.
    
    *Example* Get the type of a string.
    
        > r.expr("foo").type_of().run(conn)
        "STRING"
    
    '''
def rethinkdb.ast.RqlQuery.ungroup()
    '''grouped_stream.ungroup() -> array
    grouped_data.ungroup() -> array
    
    Takes a grouped stream or grouped data and turns it into an array of
    objects representing the groups.  Any commands chained after `ungroup`
    will operate on this array, rather than operating on each group
    individually.  This is useful if you want to e.g. order the groups by
    the value of their reduction.
    
    The format of the array returned by `ungroup` is the same as the
    default native format of grouped data in the JavaScript driver and
    data explorer.
    
    Suppose that the table `games` has the following data:
    
        [
            {"id": 2, "player": "Bob", "points": 15, "type": "ranked"},
            {"id": 5, "player": "Alice", "points": 7, "type": "free"},
            {"id": 11, "player": "Bob", "points": 10, "type": "free"},
            {"id": 12, "player": "Alice", "points": 2, "type": "free"}
        ]
    
    *Example* What is the maximum number of points scored by each
    player, with the highest scorers first?
    
        r.table(\'games\')
           .group(\'player\').max(\'points\')[\'points\']
           .ungroup().order_by(r.desc(\'reduction\')).run(conn)
    
    <!-- stop -->
    
    Result: 
    
        [
            {
                "group": "Bob",
                "reduction": 15
            },
            {
                "group": "Alice",
                "reduction": 7
            }
        ]
    
    *Example* Select one random player and all their games.
    
        r.table(\'games\').group(\'player\').ungroup().sample(1).run(conn)
    
    Result:
    
        [
            {
                "group": "Bob",
                "reduction": [
                    {"id": 2, "player": "Bob", "points": 15, "type": "ranked"},
                    {"id": 11, "player": "Bob", "points": 10, "type": "free"}
                ]
            }
        ]
    
    Note that if you didn\'t call `ungroup`, you would instead select one
    random game from each player:
    
        r.table(\'games\').group(\'player\').sample(1).run(conn)
    
    Result:
    
        {
            "Alice": [
                {"id": 5, "player": "Alice", "points": 7, "type": "free"}
            ],
            "Bob": [
                {"id": 11, "player": "Bob", "points": 10, "type": "free"}
            ]
        }
    
    *Example* Types!
    
        r.table(\'games\').group(\'player\').type_of().run(conn) # Returns "GROUPED_STREAM"
        r.table(\'games\').group(\'player\').ungroup().type_of().run(conn) # Returns "ARRAY"
        r.table(\'games\').group(\'player\').avg(\'points\').run(conn) # Returns "GROUPED_DATA"
        r.table(\'games\').group(\'player\').avg(\'points\').ungroup().run(conn) #Returns "ARRAY"
    '''
def rethinkdb.ast.RqlQuery.union()
    '''stream.union(sequence[, sequence, ...][, interleave=True]) -> stream
    array.union(sequence[, sequence, ...][, interleave=True]) -> array
    
    Merge two or more sequences.
    
    The optional `interleave` argument controls how the sequences will be merged:
    
    * `True`: results will be mixed together; this is the fastest setting, but ordering of elements is not guaranteed. (This is the default.)
    * `False`: input sequences will be appended to one another, left to right.
    * `"field_name"`: a string will be taken as the name of a field to perform a merge-sort on. The input sequences must be ordered _before_ being passed to `union`.
    
    *Example* Construct a stream of all heroes.
    
        r.table(\'marvel\').union(r.table(\'dc\')).run(conn)
    
    *Example* Combine four arrays into one.
    
        r.expr([1, 2]).union([3, 4], [5, 6], [7, 8, 9]).run(conn)
        
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    *Example* Create a changefeed from the first example.
    
        r.table(\'marvel\').union(r.table(\'dc\')).changes().run(conn)
    
    Now, when any heroes are added, modified or deleted from either table, a change notification will be sent out.
    
    *Example* Merge-sort the tables of heroes, ordered by name.
    
        r.table(\'marvel\').order_by(\'name\').union(
            r.table(\'dc\').order_by(\'name\'), interleave=\'name\'
        ).run(conn)
    '''
def rethinkdb.ast.RqlQuery.upcase()
    '''string.upcase() -> string
    
    Uppercases a string.
    
    *Example*
    
        > r.expr("Sentence about LaTeX.").upcase().run(conn)
        "SENTENCE ABOUT LATEX."
    
    __Note:__ `upcase` and `downcase` only affect ASCII characters.
    '''
def rethinkdb.ast.RqlQuery.values()
    '''singleSelection.values() -> array
    object.values() -> array
    
    Return an array containing all of an object\'s values. `values()` guarantees the values will come out in the same order as [keys](http://rethinkdb.com/api/python/keys).
    
    *Example* Get all of the values from a table row.
    
        # row: { "id": 1, "mail": "fred@example.com", "name": "fred"  }
        
        r.table(\'users\').get(1).values().run(conn)
        
        > [ 1, "fred@example.com", "fred" ]
    '''
def rethinkdb.ast.RqlQuery.with_fields()
    '''sequence.with_fields([selector1, selector2...]) -> stream
    array.with_fields([selector1, selector2...]) -> array
    
    Plucks one or more attributes from a sequence of objects, filtering out any objects in the sequence that do not have the specified fields. Functionally, this is identical to [has_fields](http://rethinkdb.com/api/python/has_fields/) followed by [pluck](http://rethinkdb.com/api/python/pluck/) on a sequence.
    
    *Example* Get a list of users and their posts, excluding any users who have not made any posts.
    
    Existing table structure:
    
        [
            { 'id': 1, 'user': 'bob', 'email': 'bob@foo.com', 'posts': [ 1, 4, 5 ] },
            { 'id': 2, 'user': 'george', 'email': 'george@foo.com' },
            { 'id': 3, 'user': 'jane', 'email': 'jane@foo.com', 'posts': [ 2, 3, 6 ] }
        ]
    
    Command and output:
    
        r.table('users').with_fields('id', 'user', 'posts').run(conn)
        
        [
            { 'id': 1, 'user': 'bob', 'posts': [ 1, 4, 5 ] },
            { 'id': 3, 'user': 'jane', 'posts': [ 2, 3, 6 ] }
        ]
    
    *Example* Use the [nested field syntax](http://rethinkdb.com/docs/nested-fields/) to get a list of users with cell phone numbers in their contacts.
    
        r.table('users').with_fields('id', 'user', {contact: {'phone': 'work'}).run(conn)
    "'''
def rethinkdb.ast.RqlQuery.without()
    '''sequence.without([selector1, selector2...]) -> stream
    array.without([selector1, selector2...]) -> array
    singleSelection.without([selector1, selector2...]) -> object
    object.without([selector1, selector2...]) -> object
    
    The opposite of pluck; takes an object or a sequence of objects, and returns them with
    the specified paths removed.
    
    *Example* Since we don't need it for this computation we'll save bandwidth and leave
    out the list of IronMan's romantic conquests.
    
        r.table('marvel').get('IronMan').without('personalVictoriesList').run(conn)
    
    *Example* Without their prized weapons, our enemies will quickly be vanquished.
    
        r.table('enemies').without('weapons').run(conn)
    
    *Example* Nested objects can be used to remove the damage subfield from the weapons and abilities fields.
    
        r.table('marvel').without({'weapons' : {'damage' : True}, 'abilities' : {'damage' : True}}).run(conn)
    
    *Example* The nested syntax can quickly become overly verbose so there's a shorthand for it.
    
        r.table('marvel').without({'weapons' : 'damage', 'abilities' : 'damage'}).run(conn)
    
    "'''
def rethinkdb.ast.RqlQuery.year()
    '''time.year() -> number
    
    Return the year of a time object.
    
    *Example* Retrieve all the users born in 1986.
    
        r.table("users").filter(lambda user:
            user["birthdate"].year() == 1986
        ).run(conn)
    
    '''
def rethinkdb.ast.RqlQuery.zip()
    '''stream.zip() -> stream
    array.zip() -> array
    
    Used to 'zip' up the result of a join by merging the 'right' fields into 'left' fields of each member of the sequence.
    
    *Example* 'zips up' the sequence by merging the left and right fields produced by a join.
    
        r.table('marvel').eq_join('main_dc_collaborator', r.table('dc')).zip().run(conn)
    "'''
def rethinkdb.ast.Table.between()
    '''table.between(lower_key, upper_key[, options]) -> table_slice
    table_slice.between(lower_key, upper_key[, options]) -> table_slice
    
    Get all documents between two keys. Accepts three optional arguments: `index`, `left_bound`, and `right_bound`. If `index` is set to the name of a secondary index, `between` will return all documents where that index\'s value is in the specified range (it uses the primary key by default). `left_bound` or `right_bound` may be set to `open` or `closed` to indicate whether or not to include that endpoint of the range (by default, `left_bound` is closed and `right_bound` is open).
    
    You may also use the special constants `r.minval` and `r.maxval` for boundaries, which represent "less than any index key" and "more than any index key" respectively. For instance, if you use `r.minval` as the lower key, then `between` will return all documents whose primary keys (or indexes) are less than the specified upper key.
    
    If you use arrays as indexes (compound indexes), they will be sorted using lexicographical order. Take the following range as an example:
    
    \t[[1, "c"] ... [5, "e"]]
    
    This range includes all compound keys:
    
    * whose first item is 1 and second item is equal or greater than "c";
    * whose first item is between 1 and 5, *regardless of the value of the second item*;
    * whose first item is 5 and second item is less than or equal to "e".
    
    *Example* Find all users with primary key >= 10 and < 20 (a normal half-open interval).
    
        r.table(\'marvel\').between(10, 20).run(conn)
    
    *Example* Find all users with primary key >= 10 and <= 20 (an interval closed on both sides).
    
        r.table(\'marvel\').between(10, 20, right_bound=\'closed\').run(conn)
    
    *Example* Find all users with primary key < 20.
    
        r.table(\'marvel\').between(r.minval, 20).run(conn)
    
    *Example* Find all users with primary key > 10.
    
        r.table(\'marvel\').between(10, r.maxval, left_bound=\'open\').run(conn)
    
    *Example* Between can be used on secondary indexes too. Just pass an optional index argument giving the secondary index to query.
    
        r.table(\'dc\').between(\'dark_knight\', \'man_of_steel\', index=\'code_name\').run(conn)
    
    *Example* Get all users whose full name is between "John Smith" and "Wade Welles."
    
        r.table("users").between(["Smith", "John"], ["Welles", "Wade"],
            index="full_name").run(conn)
    
    *Example* Get the top 10 ranked teams in order.
    
        r.table("teams").order_by(index="rank").between(1, 11).run(conn)
    
    __Note:__ When `between` is chained after [order_by](http://rethinkdb.com/api/python/order_by), both commands must use the same index; `between` will default to the index `order_by` is using, so in this example `"rank"` is automatically being used by `between`. Trying to specify another index will result in a `ReqlRuntimeError`.
    
    *Example* Subscribe to a [changefeed](http://rethinkdb.com/docs/changefeeds/python) of teams ranked in the top 10.
    
        changes = r.table("teams").between(1, 11, index="rank").changes().run(conn)
    
    '''
def rethinkdb.ast.Table.config()
    '''table.config() -> selection&lt;object&gt;
    database.config() -> selection&lt;object&gt;
    
    Query (read and/or update) the configurations for individual tables or databases.
    
    The `config` command is a shorthand way to access the `table_config` or `db_config` [System tables](http://rethinkdb.com/docs/system-tables/#configuration-tables). It will return the single row from the system that corresponds to the database or table configuration, as if [get](http://rethinkdb.com/api/python/get) had been called on the system table with the UUID of the database or table in question.
    
    *Example* Get the configuration for the `users` table.
    
        r.table(\'users\').config().run(conn)
    
    <!-- stop -->
    
    Example return:
    
        
        {
            "id": "31c92680-f70c-4a4b-a49e-b238eb12c023",
            "name": "users",
            "db": "superstuff",
            "primary_key": "id",
            "shards": [
                {
                    "primary_replica": "a",
                    "replicas": ["a", "b"],
                    "nonvoting_replicas": []
                },
                {
                    "primary_replica": "d",
                    "replicas": ["c", "d"],
                    "nonvoting_replicas": []
                }
            ],
            "indexes": [],
            "write_acks": "majority",
            "durability": "hard"
        }
    
    *Example* Change the write acknowledgement requirement of the `users` table.
    
        r.table(\'users\').config().update({\'write_acks\': \'single\'}).run(conn)
    '''
def rethinkdb.ast.Table.delete()
    '''table.delete([durability="hard", return_changes=False])
        -> object
    selection.delete([durability="hard", return_changes=False])
        -> object
    singleSelection.delete([durability="hard", return_changes=False])
        -> object
    
    Delete one or more documents from a table.
    
    The optional arguments are:
    
    - `durability`: possible values are `hard` and `soft`. This option will override the
    table or query\'s durability setting (set in [run](http://rethinkdb.com/api/python/run/)).  
    In soft durability mode RethinkDB will acknowledge the write immediately after
    receiving it, but before the write has been committed to disk.
    - `return_changes`:
        - `True`: return a `changes` array consisting of `old_val`/`new_val` objects describing the changes made, only including the documents actually updated.
        - `False`: do not return a `changes` array (the default).
        - `"always"`: behave as `True`, but include all documents the command tried to update whether or not the update was successful. (This was the behavior of `True` pre-2.0.)
    
    Delete returns an object that contains the following attributes:
    
    - `deleted`: the number of documents that were deleted.
    - `skipped`: the number of documents that were skipped.  
    For example, if you attempt to delete a batch of documents, and another concurrent query
    deletes some of those documents first, they will be counted as skipped.
    - `errors`: the number of errors encountered while performing the delete.
    - `first_error`: If errors were encountered, contains the text of the first error.
    - `inserted`, `replaced`, and `unchanged`: all 0 for a delete operation.
    - `changes`: if `return_changes` is set to `True`, this will be an array of objects, one for each objected affected by the `delete` operation. Each object will have two keys: `{"new_val": None, "old_val": <old value>}`.
    
    *Example* Delete a single document from the table `comments`.
    
        r.table("comments").get("7eab9e63-73f1-4f33-8ce4-95cbea626f59").delete().run(conn)
    
    *Example* Delete all documents from the table `comments`.
    
        r.table("comments").delete().run(conn)
    
    *Example* Delete all comments where the field `id_post` is `3`.
    
        r.table("comments").filter({"id_post": 3}).delete().run(conn)
    
    *Example* Delete a single document from the table `comments` and return its value.
    
        r.table("comments").get("7eab9e63-73f1-4f33-8ce4-95cbea626f59").delete(return_changes=True).run(conn)
    
    The result will look like:
    
        {
            "deleted": 1,
            "errors": 0,
            "inserted": 0,
            "changes": [
                {
                    "new_val": None,
                    "old_val": {
                        "id": "7eab9e63-73f1-4f33-8ce4-95cbea626f59",
                        "author": "William",
                        "comment": "Great post",
                        "id_post": 3
                    }
                }
            ],
            "replaced": 0,
            "skipped": 0,
            "unchanged": 0
        }
    
    *Example* Delete all documents from the table `comments` without waiting for the
    operation to be flushed to disk.
    
        r.table("comments").delete(durability="soft"}).run(conn)
    '''
def rethinkdb.ast.Table.get()
    '''table.get(key) -> singleRowSelection
    
    Get a document by primary key.
    
    If no document exists with that primary key, `get` will return `None`.
    
    *Example* Find a document by UUID.
    
        r.table('posts').get('a9849eef-7176-4411-935b-79a6e3c56a74').run(conn)
    
    *Example* Find a document and merge another document with it.
    
        r.table('heroes').get(3).merge(
            { 'powers': ['invisibility', 'speed'] }
        ).run(conn)
    
    _*Example* Subscribe to a document's [changefeed](http://rethinkdb.com/docs/changefeeds/python).
    
        changes = r.table('heroes').get(3).changes().run(conn)
    "'''
def rethinkdb.ast.Table.get_all()
    '''table.get_all([key1, key2...], [, index='id']) -> selection
    
    Get all documents where the given value matches the value of the requested index.
    
    *Example* Secondary index keys are not guaranteed to be unique so we cannot query via [get](http://rethinkdb.com/api/python/get/) when using a secondary index.
    
        r.table('marvel').get_all('man_of_steel', index='code_name').run(conn)
    
    *Example* Without an index argument, we default to the primary index. While `get` will either return the document or `None` when no document with such a primary key value exists, this will return either a one or zero length stream.
    
        r.table('dc').get_all('superman').run(conn)
    
    *Example* You can get multiple documents in a single call to `get_all`.
    
        r.table('dc').get_all('superman', 'ant man').run(conn)
    
    *Example* You can use [args](http://rethinkdb.com/api/python/args/) with `get_all` to retrieve multiple documents whose keys are in a list. This uses `get_all` to get a list of female superheroes, coerces that to an array, and then gets a list of villains who have those superheroes as enemies.
    
        r.do(
            r.table('heroes').get_all('f', index='gender')['id'].coerce_to('array'), 
            lamdba heroines: r.table('villains').get_all(r.args(heroines))
        ).run(conn)
    
    Calling `get_all` with zero arguments&mdash;which could happen in this example if the `heroines` list had no elements&mdash;will return nothing, i.e., a zero length stream.
    
    Secondary indexes can be used in extremely powerful ways with `get_all` and other commands; read the full article on [secondary indexes](http://rethinkdb.com/docs/secondary-indexes) for examples using boolean operations, `contains` and more.
    "'''
def rethinkdb.ast.Table.get_intersecting()
    '''table.get_intersecting(geometry, index='indexname') -> selection<stream>
    
    Get all documents where the given geometry object intersects the geometry object of the requested geospatial index.
    
    The `index` argument is mandatory. This command returns the same results as `table.filter(r.row('index').intersects(geometry))`. The total number of results is limited to the array size limit which defaults to 100,000, but can be changed with the `array_limit` option to [run](http://rethinkdb.com/api/python/run).
    
    *Example* Which of the locations in a list of parks intersect `circle1`?
    
        circle1 = r.circle([-117.220406, 32.719464], 10, unit='mi')
        r.table('parks').get_intersecting(circle1, index='area').run(conn)
    "'''
def rethinkdb.ast.Table.get_nearest()
    '''table.get_nearest(point, index='indexname'[, max_results=100, max_dist=100000, unit='m', geo_system='WGS84']) -> array
    
    Get all documents where the specified geospatial index is within a certain distance of the specified point (default 100 kilometers).
    
    The `index` argument is mandatory. Optional arguments are:
    
    * `max_results`: the maximum number of results to return (default 100).
    * `unit`: Unit for the distance. Possible values are `m` (meter, the default), `km` (kilometer), `mi` (international mile), `nm` (nautical mile), `ft` (international foot).
    * `max_dist`: the maximum distance from an object to the specified point (default 100 km).
    * `geo_system`: the reference ellipsoid to use for geographic coordinates. Possible values are `WGS84` (the default), a common standard for Earth's geometry, or `unit_sphere`, a perfect sphere of 1 meter radius.
    
    The return value will be an array of two-item objects with the keys `dist` and `doc`, set to the distance between the specified point and the document (in the units specified with `unit`, defaulting to meters) and the document itself, respectively.
    
    *Example* Return a list of enemy hideouts within 5000 meters of the secret base.
    
        secret_base = r.point(-122.422876, 37.777128)
        r.table('hideouts').get_nearest(secret_base, index='location',
            max_dist=5000).run(conn)
    "'''
def rethinkdb.ast.Table.index_create()
    '''table.index_create(index_name[, index_function][, multi=False, geo=False]) -> object
    
    Create a new secondary index on a table. Secondary indexes improve the speed of many read queries at the slight cost of increased storage space and decreased write performance. For more information about secondary indexes, read the article "[Using secondary indexes in RethinkDB](http://rethinkdb.com/docs/secondary-indexes/)."
    
    RethinkDB supports different types of secondary indexes:
    
    - *Simple indexes* based on the value of a single field.
    - *Compound indexes* based on multiple fields.
    - *Multi indexes* based on arrays of values.
    - *Geospatial indexes* based on indexes of geometry objects, created when the `geo` optional argument is true.
    - Indexes based on *arbitrary expressions*.
    
    The `index_function` can be an anonymous function or a binary representation obtained from the `function` field of [index_status](http://rethinkdb.com/api/python/index_status).
    
    If successful, `create_index` will return an object of the form `{"created": 1}`. If an index by that name already exists on the table, a `ReqlRuntimeError` will be thrown.
    
    *Example* Create a simple index based on the field `post_id`.
    
        r.table(\'comments\').index_create(\'post_id\').run(conn)
    *Example* Create a simple index based on the nested field `author > name`.
    
        r.table(\'comments\').index_create(\'author_name\', r.row["author"]["name"]).run(conn)
    
    *Example* Create a geospatial index based on the field `location`.
    
        r.table(\'places\').index_create(\'location\', geo=True).run(conn)
    
    A geospatial index field should contain only geometry objects. It will work with geometry ReQL terms ([get_intersecting](http://rethinkdb.com/api/python/get_intersecting/) and [get_nearest](http://rethinkdb.com/api/python/get_nearest/)) as well as index-specific terms ([index_status](http://rethinkdb.com/api/python/index_status), [index_wait](http://rethinkdb.com/api/python/index_wait), [index_drop](http://rethinkdb.com/api/python/index_drop) and [index_list](http://rethinkdb.com/api/python/index_list)). Using terms that rely on non-geometric ordering such as [get_all](http://rethinkdb.com/api/python/get_all/), [order_by](http://rethinkdb.com/api/python/order_by/) and [between](http://rethinkdb.com/api/python/between/) will result in an error.
    
    *Example* Create a compound index based on the fields `post_id` and `date`.
    
        r.table(\'comments\').index_create(\'post_and_date\', [r.row["post_id"], r.row["date"]]).run(conn)
    
    *Example* Create a multi index based on the field `authors`.
    
        r.table(\'posts\').index_create(\'authors\', multi=True).run(conn)
    
    *Example* Create a geospatial multi index based on the field `towers`.
    
        r.table(\'networks\').index_create(\'towers\', geo=True, multi=True).run(conn)
    
    *Example* Create an index based on an arbitrary expression.
    
        r.table(\'posts\').index_create(\'authors\', lambda doc:
            r.branch(
                doc.has_fields("updated_at"),
                doc["updated_at"],
                doc["created_at"]
            )
        ).run(conn)
    
    *Example* Create a new secondary index based on an existing one.
    
        index = r.table(\'posts\').index_status(\'authors\').nth(0)[\'function\'].run(conn)
        r.table(\'new_posts\').index_create(\'authors\', index).run(conn)
    
    *Example* Rebuild an outdated secondary index on a table.
    
        old_index = r.table(\'posts\').index_status(\'old_index\').nth(0)[\'function\'].run(conn)
        r.table(\'posts\').index_create(\'new_index\', old_index).run(conn)
        r.table(\'posts\').index_wait(\'new_index\').run(conn)
        r.table(\'posts\').index_rename(\'new_index\', \'old_index\', overwrite=True).run(conn)
    '''
def rethinkdb.ast.Table.index_drop()
    '''table.index_drop(index_name) -> object
    
    Delete a previously created secondary index of this table.
    
    *Example* Drop a secondary index named 'code_name'.
    
        r.table('dc').index_drop('code_name').run(conn)
    
    "'''
def rethinkdb.ast.Table.index_list()
    '''table.index_list() -> array
    
    List all the secondary indexes of this table.
    
    *Example* List the available secondary indexes for this table.
    
        r.table('marvel').index_list().run(conn)
    "'''
def rethinkdb.ast.Table.index_rename()
    '''table.index_rename(old_index_name, new_index_name[, overwrite=False]) -> object
    
    Rename an existing secondary index on a table. If the optional argument `overwrite` is specified as `True`, a previously existing index with the new name will be deleted and the index will be renamed. If `overwrite` is `False` (the default) an error will be raised if the new index name already exists.
    
    The return value on success will be an object of the format `{'renamed': 1}`, or `{'renamed': 0}` if the old and new names are the same.
    
    An error will be raised if the old index name does not exist, if the new index name is already in use and `overwrite` is `False`, or if either the old or new index name are the same as the primary key field name.
    
    *Example* Rename an index on the comments table.
    
        r.table('comments').index_rename('post_id', 'message_id').run(conn)
    "'''
def rethinkdb.ast.Table.index_status()
    '''table.index_status([, index...]) -> array
    
    Get the status of the specified indexes on this table, or the status
    of all indexes on this table if no indexes are specified.
    
    The result is an array where for each index, there will be an object like this one:
    
        {
            "index": <index_name>,
            "ready": True,
            "function": <binary>,
            "multi": <bool>,
            "outdated": <bool>
        }
    
    or this one:
    
        {
            "index": <index_name>,
            "ready": False,
            "progress": <float>,
            "function": <binary>,
            "multi": <bool>,
            "outdated": <bool>
        }
    
    The `multi` field will be `true` or `false` depending on whether this index was created as a multi index (see [index_create](http://rethinkdb.com/api/python/index_create/) for details). The `outdated` field will be true if the index is outdated in the current version of RethinkDB and needs to be rebuilt. The `progress` field is a float between `0` and `1`, indicating how far along the server is in constructing indexes after the most recent change to the table that would affect them. (`0` indicates no such indexes have been constructed; `1` indicates all of them have.)
    
    The `function` field is a binary object containing an opaque representation of the secondary index (including the `multi` argument if specified). It can be passed as the second argument to [index_create](http://rethinkdb.com/api/python/index_create/) to create a new index with the same function; see `index_create` for more information.
    
    *Example* Get the status of all the indexes on `test`:
    
        r.table(\'test\').index_status().run(conn)
    
    *Example* Get the status of the `timestamp` index:
    
        r.table(\'test\').index_status(\'timestamp\').run(conn)
    
    *Example* Save the binary representation of the index:
    
        func = r.table(\'test\').index_status(\'timestamp\').nth(0)[\'function\'].run(conn)
    '''
def rethinkdb.ast.Table.index_wait()
    '''table.index_wait([, index...]) -> array
    
    Wait for the specified indexes on this table to be ready, or for all
    indexes on this table to be ready if no indexes are specified.
    
    The result is an array containing one object for each table index:
    
        {
            "index": <index_name>,
            "ready": True,
            "function": <binary>,
            "multi": <bool>,
            "geo": <bool>,
            "outdated": <bool>
        }
    
    See the [index_status](http://rethinkdb.com/api/python/index_status) documentation for a description of the field values.
    
    *Example* Wait for all indexes on the table `test` to be ready:
    
        r.table(\'test\').index_wait().run(conn)
    
    *Example* Wait for the index `timestamp` to be ready:
    
        r.table(\'test\').index_wait(\'timestamp\').run(conn)
    '''
def rethinkdb.ast.Table.insert()
    '''table.insert(object | [object1, object2, ...][, durability="hard", return_changes=False, conflict="error"])
        -> object
    
    Insert documents into a table. Accepts a single document or an array of
    documents.
    
    The optional arguments are:
    
    - `durability`: possible values are `hard` and `soft`. This option will override the table or query\'s durability setting (set in [run](http://rethinkdb.com/api/python/run/)). In soft durability mode RethinkDB will acknowledge the write immediately after receiving and caching it, but before the write has been committed to disk.
    - `return_changes`:
        - `True`: return a `changes` array consisting of `old_val`/`new_val` objects describing the changes made, only including the documents actually updated.
        - `False`: do not return a `changes` array (the default).
        - `"always"`: behave as `True`, but include all documents the command tried to update whether or not the update was successful. (This was the behavior of `True` pre-2.0.)
    - `conflict`: Determine handling of inserting documents with the same primary key as existing entries. Possible values are `"error"`, `"replace"` or `"update"`.
        - `"error"`: Do not insert the new document and record the conflict as an error. This is the default.
        - `"replace"`: [Replace](http://rethinkdb.com/api/python/replace/) the old document in its entirety with the new one.
        - `"update"`: [Update](http://rethinkdb.com/api/python/update/) fields of the old document with fields from the new one.
    
    If `return_changes` is set to `True` or `"always"`, the `changes` array will follow the same order as the inserted documents. Documents in `changes` for which an error occurs (such as a key conflict) will have a third field, `error`, with an explanation of the error.
    
    Insert returns an object that contains the following attributes:
    
    - `inserted`: the number of documents successfully inserted.
    - `replaced`: the number of documents updated when `conflict` is set to `"replace"` or `"update"`.
    - `unchanged`: the number of documents whose fields are identical to existing documents with the same primary key when `conflict` is set to `"replace"` or `"update"`.
    - `errors`: the number of errors encountered while performing the insert.
    - `first_error`: If errors were encountered, contains the text of the first error.
    - `deleted` and `skipped`: 0 for an insert operation.
    - `generated_keys`: a list of generated primary keys for inserted documents whose primary keys were not specified (capped to 100,000).
    - `warnings`: if the field `generated_keys` is truncated, you will get the warning _"Too many generated keys (&lt;X&gt;), array truncated to 100000."_.
    - `changes`: if `return_changes` is set to `True`, this will be an array of objects, one for each objected affected by the `insert` operation. Each object will have two keys: `{"new_val": <new value>, "old_val": None}`.
    
    *Example* Insert a document into the table `posts`.
    
        r.table("posts").insert({
            "id": 1,
            "title": "Lorem ipsum",
            "content": "Dolor sit amet"
        }).run(conn)
    
    <!-- stop -->
    
    The result will be:
    
        {
            "deleted": 0,
            "errors": 0,
            "inserted": 1,
            "replaced": 0,
            "skipped": 0,
            "unchanged": 0
        }
    
    *Example* Insert a document without a defined primary key into the table `posts` where the
    primary key is `id`.
    
        r.table("posts").insert({
            "title": "Lorem ipsum",
            "content": "Dolor sit amet"
        }).run(conn)
    
    RethinkDB will generate a primary key and return it in `generated_keys`.
    
        {
            "deleted": 0,
            "errors": 0,
            "generated_keys": [
                "dd782b64-70a7-43e4-b65e-dd14ae61d947"
            ],
            "inserted": 1,
            "replaced": 0,
            "skipped": 0,
            "unchanged": 0
        }
    
    Retrieve the document you just inserted with:
    
        r.table("posts").get("dd782b64-70a7-43e4-b65e-dd14ae61d947").run(conn)
    
    And you will get back:
    
        {
            "id": "dd782b64-70a7-43e4-b65e-dd14ae61d947",
            "title": "Lorem ipsum",
            "content": "Dolor sit amet",
        }
    
    *Example* Insert multiple documents into the table `users`.
    
        r.table("users").insert([
            {"id": "william", "email": "william@rethinkdb.com"},
            {"id": "lara", "email": "lara@rethinkdb.com"}
        ]).run(conn)
    
    *Example* Insert a document into the table `users`, replacing the document if the document
    already exists.  
    
        r.table("users").insert(
            {"id": "william", "email": "william@rethinkdb.com"},
            conflict="replace"
        ).run(conn)
    
    *Example* Copy the documents from `posts` to `posts_backup`.
    
        r.table("posts_backup").insert( r.table("posts") ).run(conn)
    
    *Example* Get back a copy of the inserted document (with its generated primary key).
    
        r.table("posts").insert(
            {"title": "Lorem ipsum", "content": "Dolor sit amet"},
            return_changes=True
        ).run(conn)
    
    The result will be
    
        {
            "deleted": 0,
            "errors": 0,
            "generated_keys": [
                "dd782b64-70a7-43e4-b65e-dd14ae61d947"
            ],
            "inserted": 1,
            "replaced": 0,
            "skipped": 0,
            "unchanged": 0,
            "changes": [
                {
                    "old_val": None,
                    "new_val": {
                        "id": "dd782b64-70a7-43e4-b65e-dd14ae61d947",
                        "title": "Lorem ipsum",
                        "content": "Dolor sit amet"
                    }
                }
            ]
        }
    '''
def rethinkdb.ast.Table.order_by()
    '''table.order_by([key | function], index=index_name) -> table_slice
    selection.order_by(key | function[, ...]) -> selection<array>
    sequence.order_by(key | function[, ...]) -> array
    
    Sort the sequence by document values of the given key(s). To specify
    the ordering, wrap the attribute with either `r.asc` or `r.desc`
    (defaults to ascending).
    
    __Note:__ RethinkDB uses byte-wise ordering for `orderBy` and does not support Unicode collations; non-ASCII characters will be sorted by UTF-8 codepoint. For more information on RethinkDB\'s sorting order, read the section in [ReQL data types](http://rethinkdb.com/docs/data-types/#sorting-order).
    
    Sorting without an index requires the server to hold the sequence in
    memory, and is limited to 100,000 documents (or the setting of the `arrayLimit` option for [run](http://rethinkdb.com/api/python/run)). Sorting with an index can
    be done on arbitrarily large tables, or after a [between](http://rethinkdb.com/api/python/between/) command
    using the same index. This applies to both secondary indexes and the primary key (e.g., `index=\'id\'`).
    
    *Example* Order all the posts using the index `date`.   
    
        r.table(\'posts\').order_by(index=\'date\').run(conn)
    
    <!-- stop -->
    
    The index must either be the primary key or have been previously created with [index_create](http://rethinkdb.com/api/python/index_create/).
    
        r.table(\'posts\').index_create(\'date\').run(conn)
    
    You can also select a descending ordering:
    
        r.table(\'posts\').order_by(index=r.desc(\'date\')).run(conn, callback)
    
    *Example* Order a sequence without an index.
    
        r.table(\'posts\').get(1)[\'comments\'].order_by(\'date\')
    
    You can also select a descending ordering:
    
        r.table(\'posts\').get(1)[\'comments\'].order_by(r.desc(\'date\'))
    
    If you\'re doing ad-hoc analysis and know your table won\'t have more then 100,000
    elements (or you\'ve changed the setting of the `arrayLimit` option for [run](http://rethinkdb.com/api/python/run)) you can run `order_by` without an index:
    
        r.table(\'small_table\').order_by(\'date\')
    
    *Example* You can efficiently order using multiple fields by using a
    [compound index](http://www.rethinkdb.com/docs/secondary-indexes/python/).
    
    Order by date and title.
    
        r.table(\'posts\').order_by(index=\'date_and_title\').run(conn)
    
    The index must either be the primary key or have been previously created with [index_create](http://rethinkdb.com/api/python/index_create/).
    
        r.table(\'posts\').index_create(\'date_and_title\', lambda post:
            [post["date"], post["title"]]).run(conn)
    
    _Note_: You cannot specify multiple orders in a compound index. See [issue #2306](https://github.com/rethinkdb/rethinkdb/issues/2306)
    to track progress.
    
    *Example* If you have a sequence with fewer documents than the `array_limit`, you can order it
    by multiple fields without an index.
    
        r.table(\'small_table\').order_by(\'date\', r.desc(\'title\'))
    
    *Example* Notice that an index ordering always has highest
    precedence. The following query orders posts by date, and if multiple
    posts were published on the same date, they will be ordered by title.
    
        r.table(\'post\').order_by(\'title\', index=\'date\').run(conn)
    *Example* You can use [nested field](http://rethinkdb.com/docs/cookbook/python/#filtering-based-on-nested-fields) syntax to sort on fields from subdocuments. (You can also create indexes on nested fields using this syntax with `index_create`.)
    
        r.table(\'user\').order_by(lambda user: user[\'group\'][\'id\']).run(conn)
    
    *Example* You can efficiently order data on arbitrary expressions using indexes.
    
        r.table(\'posts\').order_by(index=\'votes\').run(conn)
    
    The index must have been previously created with [index_create](http://rethinkdb.com/api/ruby/index_create/).
    
        r.table(\'posts\').index_create(\'votes\', lambda post:
            post["upvotes"]-post["downvotes"]
        ).run(conn)
    
    *Example* If you have a sequence with fewer documents than the `array_limit`, you can order it with an arbitrary function directly.
    
        r.table(\'small_table\').order_by(lambda doc:
            doc[\'upvotes\']-doc[\'downvotes\']
        );
    
    You can also select a descending ordering:
    
        r.table(\'small_table\').order_by(r.desc(lambda doc:
            doc[\'upvotes\']-doc[\'downvotes\']
        ));
    
    *Example* Ordering after a `between` command can be done as long as the same index is being used.
    
        r.table("posts").between(r.time(2013, 1, 1, \'+00:00\'), r.time(2013, 1, 1, \'+00:00\'), index=\'date\')
            .order_by(index=\'date\').run(conn);
    
    '''
def rethinkdb.ast.Table.rebalance()
    '''table.rebalance() -> object
    database.rebalance() -> object
    
    Rebalances the shards of a table. When called on a database, all the tables in that database will be rebalanced.
    
    The `rebalance` command operates by measuring the distribution of primary keys within a table and picking split points that will give each shard approximately the same number of documents. It won\'t change the number of shards within a table, or change any other configuration aspect for the table or the database.
    
    A table will lose availability temporarily after `rebalance` is called; use the [wait](http://rethinkdb.com/api/python/wait) command to wait for the table to become available again, or [status](http://rethinkdb.com/api/python/status) to check if the table is available for writing.
    
    RethinkDB automatically rebalances tables when the number of shards are increased, and as long as your documents have evenly distributed primary keys&mdash;such as the default UUIDs&mdash;it is rarely necessary to call `rebalance` manually. Cases where `rebalance` may need to be called include:
    
    * Tables with unevenly distributed primary keys, such as incrementing integers
    * Changing a table\'s primary key type
    * Increasing the number of shards on an empty table, then using non-UUID primary keys in that table
    
    The [web UI](http://rethinkdb.com/docs/administration-tools/) (and the [info](http://rethinkdb.com/api/python/info) command) can be used to tell you when a table\'s shards need to be rebalanced.
    
    The return value of `rebalance` is an object with two fields:
    
    * `rebalanced`: the number of tables rebalanced.
    * `status_changes`: a list of new and old table status values. Each element of the list will be an object with two fields:
        * `old_val`: The table\'s [status](http://rethinkdb.com/api/python/status) value before `rebalance` was executed. 
        * `new_val`: The table\'s `status` value after `rebalance` was executed. (This value will almost always indicate the table is unavailable.)
    
    See the [status](http://rethinkdb.com/api/python/status) command for an explanation of the objects returned in the `old_val` and `new_val` fields.
    
    *Example* Rebalance a table.
    
        r.table(\'superheroes\').rebalance().run(conn)
    
    <!-- stop -->
    
    Example return:
    
        {
          "rebalanced": 1,
          "status_changes": [
            {
              "old_val": {
                "db": "database",
                "id": "5cb35225-81b2-4cec-9eef-bfad15481265",
                "name": "superheroes",
                "shards": [
                  {
                    "primary_replica": "jeeves",
                    "replicas": [
                      {
                        "server": "jeeves",
                        "state": "ready"
                      }
                    ]
                  },
                  {
                    "primary_replica": "jeeves",
                    "replicas": [
                      {
                        "server": "jeeves",
                        "state": "ready"
                      }
                    ]
                  }
                ],
                "status": {
                  "all_replicas_ready": True,
                  "ready_for_outdated_reads": True,
                  "ready_for_reads": True,
                  "ready_for_writes": True
                }
              },
              "new_val": {
                "db": "database",
                "id": "5cb35225-81b2-4cec-9eef-bfad15481265",
                "name": "superheroes",
                "shards": [
                  {
                    "primary_replica": "jeeves",
                    "replicas": [
                      {
                        "server": "jeeves",
                        "state": "transitioning"
                      }
                    ]
                  },
                  {
                    "primary_replica": "jeeves",
                    "replicas": [
                      {
                        "server": "jeeves",
                        "state": "transitioning"
                      }
                    ]
                  }
                ],
                "status": {
                  "all_replicas_ready": False,
                  "ready_for_outdated_reads": False,
                  "ready_for_reads": False,
                  "ready_for_writes": False
                }
              }
        
            }
          ]
        }
    '''
def rethinkdb.ast.Table.reconfigure()
    '''table.reconfigure(shards=<s>, replicas=<r>[, primary_replica_tag=<t>, dry_run=False, nonvoting_replica_tags=None]) -> object
    database.reconfigure(shards=<s>, replicas=<r>[, primary_replica_tag=<t>, dry_run=False, nonvoting_replica_tags=None]) -> object
    table.reconfigure(emergency_repair=<option>, dry_run=False) -> object
    
    Reconfigure a table\'s sharding and replication.
    
    * `shards`: the number of shards, an integer from 1-64. Required.
    * `replicas`: either an integer or a mapping object. Required.
        * If `replicas` is an integer, it specifies the number of replicas per shard. Specifying more replicas than there are servers will return an error.
        * If `replicas` is an object, it specifies key-value pairs of server tags and the number of replicas to assign to those servers: `{"tag1": 2, "tag2": 4, "tag3": 2, ...}`. For more information about server tags, read [Administration tools](http://rethinkdb.com/docs/administration-tools/).
    * `primary_replica_tag`: the primary server specified by its server tag. Required if `replicas` is an object; the tag must be in the object. This must *not* be specified if `replicas` is an integer.
    * `dry_run`: if `True` the generated configuration will not be applied to the table, only returned.
    * `nonvoting_replica_tags`: replicas with these server tags will be added to the `nonvoting_replicas` list of the resulting configuration. (See [failover](http://rethinkdb.com/docs/failover) for details about non-voting replicas.)
    * `emergency_repair`: Used for the Emergency Repair mode. See the separate section below.
    
    The return value of `reconfigure` is an object with three fields:
    
    * `reconfigured`: the number of tables reconfigured. This will be `0` if `dry_run` is `True`.
    * `config_changes`: a list of new and old table configuration values. Each element of the list will be an object with two fields:
        * `old_val`: The table\'s [config](http://rethinkdb.com/api/python/config) value before `reconfigure` was executed. 
        * `new_val`: The table\'s `config` value after `reconfigure` was executed.
    * `status_changes`: a list of new and old table status values. Each element of the list will be an object with two fields:
        * `old_val`: The table\'s [status](http://rethinkdb.com/api/python/status) value before `reconfigure` was executed. 
        * `new_val`: The table\'s `status` value after `reconfigure` was executed.
    
    For `config_changes` and `status_changes`, see the [config](http://rethinkdb.com/api/python/config) and [status](http://rethinkdb.com/api/python/status) commands for an explanation of the objects returned in the `old_val` and `new_val` fields.
    
    A table will lose availability temporarily after `reconfigure` is called; use the [wait](http://rethinkdb.com/api/python/wait) command to wait for the table to become available again, or [status](http://rethinkdb.com/api/python/status) to check if the table is available for writing.
    
    **Note:** Whenever you call `reconfigure`, the write durability will be set to `hard` and the write acknowledgments will be set to `majority`; these can be changed by using the `config` command on the table.
    
    If `reconfigure` is called on a database, all the tables in the database will have their configurations affected. The return value will be an array of the objects described above, one per table.
    
    Read [Sharding and replication](http://rethinkdb.com/docs/sharding-and-replication/) for a complete discussion of the subject, including advanced topics.
    
    *Example* Reconfigure a table.
    
        r.table(\'superheroes\').reconfigure(shards=2, replicas=1).run(conn)
    
    <!-- stop -->
    
    Example return:
    
        {
          "reconfigured": 1,
          "config_changes": [
            {
              "new_val": {
                "id": "31c92680-f70c-4a4b-a49e-b238eb12c023",
                "name": "superheroes",
                "db": "superstuff",
                "primary_key": "id",
                "shards": [
                  {
                    "primary_replica": "jeeves",
                    "replicas": ["jeeves", "alfred"],
                    "nonvoting_replicas": []
                  },
                  {
                    "primary_replica": "alfred",
                    "replicas": ["jeeves", "alfred"],
                    "nonvoting_replicas": []
                  }
                ],
                "indexes": [],
                "write_acks": "majority",
                "durability": "hard"
              },
              "old_val": {
                "id": "31c92680-f70c-4a4b-a49e-b238eb12c023",
                "name": "superheroes",
                "db": "superstuff",
                "primary_key": "id",
                "shards": [
                  {
                    "primary_replica": "alfred",
                    "replicas": ["jeeves", "alfred"],
                    "nonvoting_replicas": []
                  }
                ],
                "indexes": [],
                "write_acks": "majority",
                "durability": "hard"
              }
            }
          ],
          "status_changes": [
            {
              "new_val": (status object),
              "old_val": (status object)
            }
          ]
        }
    
    *Example* Reconfigure a table, specifying replicas by server tags.
    
        r.table(\'superheroes\').reconfigure(shards=2, replicas={\'wooster\': 1, \'wayne\': 1}, primary_replica_tag=\'wooster\').run(conn)
        
        {
          "reconfigured": 1,
          "config_changes": [
            {
              "new_val": {
                "id": "31c92680-f70c-4a4b-a49e-b238eb12c023",
                "name": "superheroes",
                "db": "superstuff",
                "primary_key": "id",
                "shards": [
                  {
                    "primary_replica": "jeeves",
                    "replicas": ["jeeves", "alfred"],
                    "nonvoting_replicas": []
                  },
                  {
                    "primary_replica": "alfred",
                    "replicas": ["jeeves", "alfred"],
                    "nonvoting_replicas": []
                  }
                ],
                "indexes": [],
                "write_acks": "majority",
                "durability": "hard"
              },
              "old_val": {
                "id": "31c92680-f70c-4a4b-a49e-b238eb12c023",
                "name": "superheroes",
                "db": "superstuff",
                "primary_key": "id",
                "shards": [
                  {
                    "primary_replica": "alfred",
                    "replicas": ["jeeves", "alfred"],
                    "nonvoting_replicas": []
                  }
                ],
                "indexes": [],
                "write_acks": "majority",
                "durability": "hard"
              }
            }
          ],
          "status_changes": [
            {
              "new_val": (status object),
              "old_val": (status object)
            }
          ]
        }
    
    RethinkDB supports automatic failover when more than half of the voting replicas for each shard of a table are still available (see the Failover documentation for more details). However, if half or more of the voting replicas for a shard are lost, failover will not happen automatically, leaving two options:
    
    * Bring enough of the missing servers back online to allow automatic failover
    * Use emergency repair mode to reconfigure the table
    
    The `emergency_repair` argument is effectively a different command; when it is specified, no other arguments to `reconfigure` are allowed except for `dry_run`. When it\'s executed, each shard of the table is examined and classified into one of three categories:
    
    * **Healthy:** more than half of the shard\'s voting replicas are still available.
    * **Repairable:** the shard is not healthy, but has at least one replica, whether voting or non-voting, available.
    * **Beyond repair:** the shard has no replicas available.
    
    For each repairable shard, `emergency_repair` will convert all unavailable voting replicas into non-voting replicas. If all the voting replicas were removed, an arbitrarily-chosen available non-voting replica will be converted into a voting replica. After this operation, all of the shard\'s available replicas will be voting replicas.
    
    Specify `emergency_repair` with one of two string options:
    
    * `unsafe_rollback`: shards that are beyond repair will be left alone.
    * `unsafe_rollback_or_erase`: a shard that is beyond repair will be destroyed and recreated on an available server that holds another shard for that table.
    
    The return value of `reconfigure` in emergency repair mode is the same as before. Examine the `config_changes` field to see the old and new configuration settings for the table. As in the normal mode, if you specify `emergency_repair` with `dry_run: True`, the table will not actually be reconfigured.
    
    __Note:__ `emergency_repair` may only be used on individual tables, not on databases. It cannot be used after the `db` command.
    
    *Example* Perform an emergency repair on a table.
    
        r.table(\'superheroes\').reconfigure(emergency_repair=\'unsafe_rollback\').run(conn)
    '''
def rethinkdb.ast.Table.replace()
    '''table.replace(object | function[, durability="hard", return_changes=False, non_atomic=False])
        -> object
    selection.replace(object | function[, durability="hard", return_changes=False, non_atomic=False])
        -> object
    singleSelection.replace(object | function[, durability="hard", return_changes=False, non_atomic=False])
        -> object
    
    Replace documents in a table. Accepts a JSON document or a ReQL expression,
    and replaces the original document with the new one. The new document must
    have the same primary key as the original document.
    
    The `replace` command can be used to both insert and delete documents. If
    the "replaced" document has a primary key that doesn\'t exist in the table,
    the document will be inserted; if an existing document is replaced with
    `None`, the document will be deleted. Since `update` and `replace` operations
    are performed atomically, this allows atomic inserts and deletes as well.
    
    The optional arguments are:
    
    - `durability`: possible values are `hard` and `soft`. This option will override
      the table or query\'s durability setting (set in [run](http://rethinkdb.com/api/python/run/)). In
      soft durability mode RethinkDB will acknowledge the write immediately after
      receiving it, but before the write has been committed to disk.
    - `return_changes`:
        - `True`: return a `changes` array consisting of `old_val`/`new_val` objects
          describing the changes made, only including the documents actually
          updated.
        - `False`: do not return a `changes` array (the default).
        - `"always"`: behave as `True`, but include all documents the command tried
          to update whether or not the update was successful. (This was the behavior
          of `True` pre-2.0.)
    - `non_atomic`: if set to `True`, executes the replacement and distributes the
      result to replicas in a non-atomic fashion. This flag is required to perform
      non-deterministic updates, such as those that require reading data from
      another table.
    
    Replace returns an object that contains the following attributes:
    
    - `replaced`: the number of documents that were replaced.
    - `unchanged`: the number of documents that would have been modified, except
      that the new value was the same as the old value.
    - `inserted`: the number of new documents added. A document is considered inserted if its primary key did not exist in the table at the time of the `replace` operation.
    - `deleted`: the number of deleted documents when doing a replace with `None`.
    - `errors`: the number of errors encountered while performing the replace.
    - `first_error`: If errors were encountered, contains the text of the first
      error.
    - `skipped`: 0 for a replace operation.
    - `changes`: if `return_changes` is set to `True`, this will be an array of
      objects, one for each objected affected by the `replace` operation. Each
      object will have two keys: `{"new_val": <new value>, "old_val": <old value>}`.
    
    *Example* Replace the document with the primary key `1`.
    
        r.table("posts").get(1).replace({
            "id": 1,
            "title": "Lorem ipsum",
            "content": "Aleas jacta est",
            "status": "draft"
        }).run(conn)
    
    *Example* Remove the field `status` from all posts.
    
        r.table("posts").replace(lambda post:
            post.without("status")
        ).run(conn)
    
    *Example* Remove all the fields that are not `id`, `title` or `content`.
    
        r.table("posts").replace(lambda post:
            post.pluck("id", "title", "content")
        ).run(conn)
    
    *Example* Replace the document with the primary key `1` using soft durability.
    
        r.table("posts").get(1).replace({
            "id": 1,
            "title": "Lorem ipsum",
            "content": "Aleas jacta est",
            "status": "draft"
        }, durability="soft").run(conn)
    
    *Example* Replace the document with the primary key `1` and return the values of the document before
    and after the replace operation.
    
        r.table("posts").get(1).replace({
            "id": 1,
            "title": "Lorem ipsum",
            "content": "Aleas jacta est",
            "status": "published"
        }, return_changes=True).run(conn)
    
    The result will have a `changes` field:
    
        {
            "deleted": 0,
            "errors":  0,
            "inserted": 0,
            "changes": [
                {
                    "new_val": {
                        "id":1,
                        "title": "Lorem ipsum"
                        "content": "Aleas jacta est",
                        "status": "published",
                    },
                    "old_val": {
                        "id":1,
                        "title": "Lorem ipsum"
                        "content": "TODO",
                        "status": "draft",
                        "author": "William",
                    }
                }
            ],   
            "replaced": 1,
            "skipped": 0,
            "unchanged": 0
        }
    '''
def rethinkdb.ast.Table.status()
    '''table.status() -> selection&lt;object&gt;
    
    Return the status of a table.
    
    The return value is an object providing information about the table\'s shards, replicas and replica readiness states. For a more complete discussion of the object fields, read about the `table_status` table in [System tables](http://rethinkdb.com/docs/system-tables/#status-tables).
    
    * `id`: the UUID of the table.
    * `name`: the table\'s name.
    * `db`: the database the table is in.
    * `status`: the subfields in this field indicate whether all shards of the table are ready to accept the given type of query: `outdated_reads`, `reads` and `writes`. The `all_replicas_ready` field indicates whether all backfills have finished.
    * `shards`: one entry for each shard in `table_config`. Each shard\'s object has the following fields:
    \t* `primary_replicas`: a list of zero or more servers acting as primary replicas for the table.
    \t* `replicas`: a list of all servers acting as a replica for that shard. The `state` field may be one of the following: `ready`, `transitioning`, `backfilling`, `disconnected`, `waiting_for_primary`, or `waiting_for_quorum`.
    
    *Example* Get a table\'s status.
    
        r.table(\'superheroes\').status().run(conn)
    
    <!-- stop -->
    
    Example return:
    
        {
          "db": "database",
          "id": "5cb35225-81b2-4cec-9eef-bfad15481265",
          "name": "superheroes",
          "shards": [
            {
              "primary_replicas": ["jeeves"],
              "replicas": [
                {
                  "server": "jeeves",
                  "state": "ready"
                }
              ]
            },
            {
              "primary_replicas": ["jeeves"],
              "replicas": [
                {
                  "server": "jeeves",
                  "state": "ready"
                }
              ]
            }
          ],
          "status": {
            "all_replicas_ready": True,
            "ready_for_outdated_reads": True,
            "ready_for_reads": True,
            "ready_for_writes": True
          }
        }
    '''
def rethinkdb.ast.Table.sync()
    '''table.sync() -> object
    
    `sync` ensures that writes on a given table are written to permanent storage. Queries
    that specify soft durability (`durability=\'soft\'`) do not give such guarantees, so
    `sync` can be used to ensure the state of these queries. A call to `sync` does not return
    until all previous writes to the table are persisted.
    
    If successful, the operation returns an object: `{"synced": 1}`.
    
    *Example* After having updated multiple heroes with soft durability, we now want to wait
    until these changes are persisted.
    
        r.table(\'marvel\').sync().run(conn)
    
    '''
def rethinkdb.ast.Table.update()
    '''table.update(object | function[, durability="hard", return_changes=False, non_atomic=False])
        -> object
    selection.update(object | function[, durability="hard", return_changes=False, non_atomic=False])
        -> object
    singleSelection.update(object | function[, durability="hard", return_changes=False, non_atomic=False])
        -> object
    
    Update JSON documents in a table. Accepts a JSON document, a ReQL expression, or a combination of the two.
    
    The optional arguments are:
    
    - `durability`: possible values are `hard` and `soft`. This option will override the table or query\'s durability setting (set in [run](http://rethinkdb.com/api/python/run/)). In soft durability mode RethinkDB will acknowledge the write immediately after receiving it, but before the write has been committed to disk.
    - `return_changes`:
        - `True`: return a `changes` array consisting of `old_val`/`new_val` objects describing the changes made, only including the documents actually updated.
        - `False`: do not return a `changes` array (the default).
        - `"always"`: behave as `True`, but include all documents the command tried to update whether or not the update was successful. (This was the behavior of `True` pre-2.0.)
    - `non_atomic`: if set to `True`, executes the update and distributes the result to replicas in a non-atomic fashion. This flag is required to perform non-deterministic updates, such as those that require reading data from another table.
    
    Update returns an object that contains the following attributes:
    
    - `replaced`: the number of documents that were updated.
    - `unchanged`: the number of documents that would have been modified except the new value was the same as the old value.
    - `skipped`: the number of documents that were skipped because the document didn\'t exist.
    - `errors`: the number of errors encountered while performing the update.
    - `first_error`: If errors were encountered, contains the text of the first error.
    - `deleted` and `inserted`: 0 for an update operation.
    - `changes`: if `return_changes` is set to `True`, this will be an array of objects, one for each objected affected by the `update` operation. Each object will have two keys: `{"new_val": <new value>, "old_val": <old value>}`.
    
    *Example* Update the status of the post with `id` of `1` to `published`.
    
        r.table("posts").get(1).update({"status": "published"}).run(conn)
    
    *Example* Update the status of all posts to `published`.
    
        r.table("posts").update({"status": "published"}).run(conn)
    
    *Example* Update the status of all the posts written by William.
    
        r.table("posts").filter({"author": "William"}).update({"status": "published"}).run(conn)
    
    *Example* Increment the field `view` of the post with `id` of `1`.
    This query will throw an error if the field `views` doesn\'t exist.
    
        r.table("posts").get(1).update({
            "views": r.row["views"]+1
        }).run(conn)
    
    *Example* Increment the field `view` of the post with `id` of `1`.
    If the field `views` does not exist, it will be set to `0`.
    
        r.table("posts").get(1).update({
            "views": (r.row["views"]+1).default(0)
        }).run(conn)
    
    *Example* Perform a conditional update.  
    If the post has more than 100 views, set the `type` of a post to `hot`, else set it to `normal`.
    
        r.table("posts").get(1).update(lambda post:
            r.branch(
                post["views"] > 100,
                {"type": "hot"},
                {"type": "normal"}
            )
        ).run(conn)
    
    *Example* Update the field `num_comments` with the result of a sub-query. Because this update is not atomic, you must pass the `non_atomic` flag.
    
        r.table("posts").get(1).update({
            "num_comments": r.table("comments").filter({"id_post": 1}).count()
        }, non_atomic=True).run(conn)
    
    If you forget to specify the `non_atomic` flag, you will get a `ReqlRuntimeError`:
    
    ReqlRuntimeError: Could not prove function deterministic.  Maybe you want to use the non_atomic flag? 
    
    *Example* Update the field `num_comments` with a random value between 0 and 100. This update cannot be proven deterministic because of `r.js` (and in fact is not), so you must pass the `non_atomic` flag.
    
        r.table("posts").get(1).update({
            "num_comments": r.js("Math.floor(Math.random()*100)")
        }, non_atomic=True).run(conn)
    
    *Example* Update the status of the post with `id` of `1` using soft durability.
    
        r.table("posts").get(1).update({status: "published"}, durability="soft").run(conn)
    
    *Example* Increment the field `views` and return the values of the document before and after the update operation.
    
        r.table("posts").get(1).update({
            "views": r.row["views"]+1
        }, return_changes=True).run(conn)
    
    The result will now include a `changes` field:
    
        {
            "deleted": 0,
            "errors": 0,
            "inserted": 0,
            "changes": [
                {
                    "new_val": {
                        "id": 1,
                        "author": "Julius_Caesar",
                        "title": "Commentarii de Bello Gallico",
                        "content": "Aleas jacta est",
                        "views": 207
                    },
                    "old_val": {
                        "id": 1,
                        "author": "Julius_Caesar",
                        "title": "Commentarii de Bello Gallico",
                        "content": "Aleas jacta est",
                        "views": 206
                    }
                }
            ],
            "replaced": 1,
            "skipped": 0,
            "unchanged": 0
        }
    
    The `update` command supports RethinkDB\'s nested field syntax to update subdocuments. Consider a user table with contact information in this format:
    
        {
            "id": 10001,
            "name": "Bob Smith",
            "contact": {
                "phone": {
                    "work": "408-555-1212",
                    "home": "408-555-1213",
                    "cell": "408-555-1214"
                },
                "email": {
                    "work": "bob@smith.com",
                    "home": "bobsmith@example.com",
                    "other": "bobbys@moosecall.net"
                },
                "im": {
                    "skype": "Bob Smith",
                    "aim": "bobmoose",
                    "icq": "nobodyremembersicqnumbers"
                }
            },
            "notes": [
                {
                    "date": r.time(2014,1,1,\'Z\'),
                    "from": "John Doe",
                    "subject": "My name is even more boring than Bob\'s"
                },
                {
                    "date": r.time(2014,2,2,\'Z\'),
                    "from": "Bob Smith Sr",
                    "subject": "Happy Second of February"
                }
            ]
        }
    
    *Example* Update Bob Smith\'s cell phone number.
    
        r.table("users").get(10001).update(
            {"contact": {"phone": {"cell": "408-555-4242"}}}
        ).run(conn)
    
    *Example* Add another note to Bob Smith\'s record.
    
        new_note = {
            "date": r.now(),
            "from": "Inigo Montoya",
            "subject": "You killed my father"
        }
        r.table("users").get(10001).update(
            {"notes": r.row["notes"].append(new_note)}
        ).run(conn)
    
    *Example* Send a note to every user with an ICQ number.
    
        icq_note = {
            "date": r.now(),
            "from": "Admin",
            "subject": "Welcome to the future"
        }
        r.table("users").filter(
            r.row.has_fields({"contact": {"im": "icq"}})
        ).update(
            {"notes": r.row["notes"].append(icq_note)}
        ).run(conn)
    
    *Example* Replace all of Bob\'s IM records. Normally, `update` will merge nested documents together; to replace the entire `"im"` document, use the literal command.
    
        r.table(\'users\').get(10001).update(
            {"contact": {"im": r.literal({"aim": "themoosemeister"})}}
        ).run(conn)
    '''
def rethinkdb.ast.Table.wait()
    '''table.wait([wait_for=\'ready_for_writes\', timeout=<sec>]) -> object
    database.wait([wait_for=\'ready_for_writes\', timeout=<sec>]) -> object
    r.wait(table | database, [wait_for=\'ready_for_writes\', timeout=<sec>]) -> object
    
    Wait for a table or all the tables in a database to be ready. A table may be temporarily unavailable after creation, rebalancing or reconfiguring. The `wait` command blocks until the given table (or database) is fully up to date.
    
    The `wait` command takes two optional arguments:
    
    * `wait_for`: a string indicating a table [status](http://rethinkdb.com/api/python/status) to wait on before returning, one of `ready_for_outdated_reads`, `ready_for_reads`, `ready_for_writes`, or `all_replicas_ready`. The default is `ready_for_writes`. 
    * `timeout`: a number indicating maximum time, in seconds, to wait for the table to be ready. If this value is exceeded, a `ReqlRuntimeError` will be thrown. A value of`0` means no timeout. The default is `0` (no timeout).
    
    The return value is an object consisting of a single field, `ready`. The value is an integer indicating the number of tables waited for. It will always be `1` when `wait` is called on a table, and the total number of tables when called on a database.
    
    *Example* Wait on a table to be ready.
    
        r.table(\'superheroes\').wait().run(conn)
        
        {"ready": 1}
    '''
def rethinkdb.binary()
    '''r.binary(data) -> binary
    
    Encapsulate binary data within a query.
    
    The type of data `binary` accepts depends on the client language. In Python, it expects a parameter of `bytes` type. Using a `bytes` object within a query implies the use of `binary` and the ReQL driver will automatically perform the coercion (in Python 3 only).
    
    Binary objects returned to the client in JavaScript will also be of the `bytes` type. This can be changed with the `binary_format` option provided to [run](http://rethinkdb.com/api/python/run) to return "raw" objects.
    
    Only a limited subset of ReQL commands may be chained after `binary`:
    
    * [coerce_to](http://rethinkdb.com/api/python/coerce_to/) can coerce `binary` objects to `string` types
    * [count](http://rethinkdb.com/api/python/count/) will return the number of bytes in the object
    * [slice](http://rethinkdb.com/api/python/slice/) will treat bytes like array indexes (i.e., `slice(10,20)` will return bytes 10&ndash;19)
    * [type_of](http://rethinkdb.com/api/python/type_of) returns `PTYPE<BINARY>`
    * [info](http://rethinkdb.com/api/python/info) will return information on a binary object.
    
    *Example* Save an avatar image to a existing user record.
    
        f = open(\'./default_avatar.png\', \'rb\')
        avatar_image = f.read()
        f.close()
        r.table(\'users\').get(100).update({\'avatar\': r.binary(avatar_image)}).run(conn)
    
    *Example* Get the size of an existing avatar image.
    
        r.table(\'users\').get(100)[\'avatar\'].count().run(conn)
        
        14156
    
    Read more details about RethinkDB\'s binary object support: [Storing binary objects](http://rethinkdb.com/docs/storing-binary/).
    '''
def rethinkdb.branch()
    '''r.branch(test, true_action[, test2, test2_action, ...], false_action) -> any
    test.branch(true_action[, test2, test2_action, ...], false_action) -> any
    
    Perform a branching conditional equivalent to `if-then-else`.
    
    The `branch` command takes 2n+1 arguments: pairs of conditional expressions and commands to be executed if the conditionals return any value but `False` or `None` (i.e., "truthy" values), with a final "else" command to be evaluated if all of the conditionals are `False` or `None`.
    
    <!-- break -->
    
    You may call `branch` infix style on the first test. (See the second example for an illustration.)
    
    r.branch(test1, val1, test2, val2, elseval)
    
    is the equivalent of the Python statement
    
        if test1:
            return val1
        elif test2:
            return val2
        else:
            return elseval
    
    *Example* Test the value of x.
    
        x = 10
        r.branch((x > 5), \'big\', \'small\').run(conn)
        
        > "big"
    
    *Example* As above, infix-style.
    
        x = 10
        r.expr(x > 5).branch(\'big\', \'small\').run(conn)
        
        > "big"
    
    *Example* Categorize heroes by victory counts.
    
        r.table(\'marvel\').map(
            r.branch(
                r.row[\'victories\'] > 100,
                r.row[\'name\'] + \' is a superhero\',
                r.row[\'victories\'] > 10,
                r.row[\'name\'] + \' is a hero\',
                r.row[\'name\'] + \' is very nice\'
            )
        ).run(conn)
    
    If the documents in the table `marvel` are:
    
        [
            { "name": "Iron Man", "victories": 214 },
            { "name": "Jubilee", "victories": 49 },
            { "name": "Slava", "victories": 5 }
        ]
    
    The results will be:
    
        [
            "Iron Man is a superhero",
            "Jubilee is a hero",
            "Slava is very nice"
        ]
    '''
def rethinkdb.circle()
    '''r.circle([longitude, latitude], radius[, num_vertices=32, geo_system='WGS84', unit='m', fill=True]) -> geometry
    r.circle(point, radius[, {num_vertices=32, geo_system='WGS84', unit='m', fill=True]) -> geometry
    
    Construct a circular line or polygon. A circle in RethinkDB is a polygon or line *approximating* a circle of a given radius around a given center, consisting of a specified number of vertices (default 32).
    
    The center may be specified either by two floating point numbers, the latitude (&minus;90 to 90) and longitude (&minus;180 to 180) of the point on a perfect sphere (see [Geospatial support](http://rethinkdb.com/docs/geo-support/) for more information on ReQL's coordinate system), or by a point object. The radius is a floating point number whose units are meters by default, although that may be changed with the `unit` argument.
    
    Optional arguments available with `circle` are:
    
    * `num_vertices`: the number of vertices in the polygon or line. Defaults to 32.
    * `geo_system`: the reference ellipsoid to use for geographic coordinates. Possible values are `WGS84` (the default), a common standard for Earth's geometry, or `unit_sphere`, a perfect sphere of 1 meter radius.
    * `unit`: Unit for the radius distance. Possible values are `m` (meter, the default), `km` (kilometer), `mi` (international mile), `nm` (nautical mile), `ft` (international foot).
    * `fill`: if `True` (the default) the circle is filled, creating a polygon; if `False` the circle is unfilled (creating a line).
    
    *Example* Define a circle.
    
        r.table('geo').insert({
            'id': 300,
            'name': 'Hayes Valley',
            'neighborhood': r.circle([-122.423246, 37.779388], 1000)
        }).run(conn)
    "'''
def rethinkdb.connect()
    '''r.connect(host="localhost", port=28015, db="test", auth_key="", timeout=20) -> connection
    r.connect(host) -> connection
    
    Create a new connection to the database server. The keyword arguments are:
    
    - `host`: host of the RethinkDB instance. The default value is `localhost`.
    - `port`: the driver port, by default `28015`.
    - `db`: the database used if not explicitly specified in a query, by default `test`.
    - `user`: the user account to connect as (default `admin`).
    - `password`: the password for the user account to connect as (default `\'\'`, empty).
    - `timeout`: timeout period in seconds for the connection to be opened (default `20`).
    - `ssl`: a hash of options to support SSL connections (default `None`). Currently, there is only one option available, and if the `ssl` option is specified, this key is required:
        - `ca_certs`: a path to the SSL CA certificate.
    
    If the connection cannot be established, a `ReqlDriverError` exception will be thrown.
    
    <!-- break -->
    
    The RethinkDB Python driver includes support for asynchronous connections using Tornado and Twisted. Read the asynchronous connections documentation for more information.
    
    *Example* Open a connection using the default host and port, specifying the default database.
    
        conn = r.connect(db=\'marvel\')
    
    *Example* Open a new connection to the database.
    
        conn = r.connect(host=\'localhost\',
                         port=28015,
                         db=\'heroes\')
    
    *Example* Open a new connection to the database, specifying a user/password combination for authentication.
    
        conn = r.connect(host=\'localhost\',
                         port=28015,
                         db=\'heroes\',
                         user=\'herofinder\',
                         password=\'metropolis\')
    
    *Example* Open a new connection to the database using an SSL proxy.
    
        conn = r.connect(host=\'localhost\',
                         port=28015,
                         auth_key=\'hunter2\',
                         ssl={\'ca_certs\': \'/path/to/ca.crt\'})
    
    *Example* Use a `with` statement to open a connection and pass it to a block. Using this style, the connection will be automatically closed when execution reaches the end of the block.
    
        with r.connect(db=\'marvel\') as conn:
            r.table(\'superheroes\').run(conn)
    '''
def rethinkdb.db()
    '''r.db(db_name) -> db
    
    Reference a database.
    
    The `db` command is optional. If it is not present in a query, the query will run against the database specified in the `db` argument given to [run](http://rethinkdb.com/api/python/run) if one was specified. Otherwise, the query will run against the default database for the connection, specified in the `db` argument to [connect](http://rethinkdb.com/api/python/connect).
    
    *Example* Explicitly specify a database for a query.
    
        r.db('heroes').table('marvel').run(conn)
    
    "'''
def rethinkdb.db_create()
    '''r.db_create(db_name) -> object
    
    Create a database. A RethinkDB database is a collection of tables, similar to
    relational databases.
    
    If successful, the command returns an object with two fields:
    
    * `dbs_created`: always `1`.
    * `config_changes`: a list containing one object with two fields, `old_val` and `new_val`:
        * `old_val`: always `None`.
        * `new_val`: the database\'s new [config](http://rethinkdb.com/api/python/config) value.
    
    If a database with the same name already exists, the command throws `ReqlRuntimeError`.
    
    Note: Only alphanumeric characters and underscores are valid for the database name.
    
    *Example* Create a database named \'superheroes\'.
    
        r.db_create(\'superheroes\').run(conn)
        
        {
            "config_changes": [
                {
                    "new_val": {
                        "id": "e4689cfc-e903-4532-a0e6-2d6797a43f07",
                        "name": "superheroes"
                    },
                    "old_val": None
                }
            ],
            "dbs_created": 1
        }
    
    '''
def rethinkdb.db_drop()
    '''r.db_drop(db_name) -> object
    
    Drop a database. The database, all its tables, and corresponding data will be deleted.
    
    If successful, the command returns an object with two fields:
    
    * `dbs_dropped`: always `1`.
    * `tables_dropped`: the number of tables in the dropped database.
    * `config_changes`: a list containing one two-field object, `old_val` and `new_val`:
        * `old_val`: the database\'s original [config](http://rethinkdb.com/api/python/config) value.
        * `new_val`: always `None`.
    
    If the given database does not exist, the command throws `ReqlRuntimeError`.
    
    *Example* Drop a database named \'superheroes\'.
    
        r.db_drop(\'superheroes\').run(conn)
        
        {
            "config_changes": [
                {
                    "old_val": {
                        "id": "e4689cfc-e903-4532-a0e6-2d6797a43f07",
                        "name": "superheroes"
                    },
                    "new_val": None
                }
            ],
            "tables_dropped": 3,
            "dbs_dropped": 1
        }
    
    '''
def rethinkdb.db_list()
    '''r.db_list() -> array
    
    List all database names in the system. The result is a list of strings.
    
    *Example* List all databases.
    
        r.db_list().run(conn)
    
    '''
def rethinkdb.div()
    '''number / number -> number
    number.div(number[, number ...]) -> number
    
    Divide two numbers.
    
    *Example* It's as easy as 2 / 2 = 1.
    
        (r.expr(2) / 2).run(conn)
    "'''
def rethinkdb.epoch_time()
    '''r.epoch_time(number) -> time
    
    Create a time object based on seconds since epoch. The first argument is a double and
    will be rounded to three decimal places (millisecond-precision).
    
    *Example* Update the birthdate of the user "John" to November 3rd, 1986.
    
        r.table("user").get("John").update({"birthdate": r.epoch_time(531360000)}).run(conn)
    
    '''
def rethinkdb.error()
    '''r.error(message) -> error
    
    Throw a runtime error. If called with no arguments inside the second argument to `default`, re-throw the current error.
    
    *Example* Iron Man can't possibly have lost a battle:
    
        r.table('marvel').get('IronMan').do(
            lambda ironman: r.branch(ironman['victories'] < ironman['battles'],
                                     r.error('impossible code path'),
                                     ironman)
        ).run(conn)
    
    "'''
def rethinkdb.expr()
    '''r.expr(value) -> value
    
    Construct a ReQL JSON object from a native object.
    
    If the native object is of the `bytes` type, then `expr` will return a binary object. See [binary](http://rethinkdb.com/api/python/binary) for more information.
    
    *Example* Objects wrapped with `expr` can then be manipulated by ReQL API functions.
    
        r.expr({'a':'b'}).merge({'b':[1,2,3]}).run(conn)
    
    "'''
def rethinkdb.geojson()
    '''r.geojson(geojson) -> geometry
    
    Convert a [GeoJSON](http://geojson.org) object to a ReQL geometry object.
    
    RethinkDB only allows conversion of GeoJSON objects which have ReQL equivalents: Point, LineString, and Polygon. MultiPoint, MultiLineString, and MultiPolygon are not supported. (You could, however, store multiple points, lines and polygons in an array and use a geospatial multi index with them.)
    
    Only longitude/latitude coordinates are supported. GeoJSON objects that use Cartesian coordinates, specify an altitude, or specify their own coordinate reference system will be rejected.
    
    *Example* Convert a GeoJSON object to a ReQL geometry object.
    
        geo_json = {
            'type': 'Point',
            'coordinates': [ -122.423246, 37.779388 ]
        }
        r.table('geo').insert({
            'id': 'sfo',
            'name': 'San Francisco',
            'location': r.geojson(geo_json)
        }).run(conn)
    "'''
def rethinkdb.grant()
    '''r.grant("username", {"permission": bool[, ...]}) -> object
    db.grant("username", {"permission": bool[, ...]}) -> object
    table.grant("username", {"permission": bool[, ...]}) -> object
    
    Grant or deny access permissions for a user account, globally or on a per-database or per-table basis.
    
    There are four different permissions that can be granted to an account:
    
    * `read` allows reading the data in tables.
    * `write` allows modifying data, including inserting, replacing/updating, and deleting.
    * `connect` allows a user to open HTTP connections via the http command. This permission can only be granted in global scope.
    * `config` allows users to create/drop secondary indexes on a table and changing the cluster configuration; to create and drop tables, if granted on a database; and to create and drop databases, if granted globally.
    
    Permissions may be granted on a global scope, or granted for a specific table or database. The scope is defined by calling `grant` on its own (e.g., `r.grant()`, on a table (`r.table().grant()`), or on a database (`r.db().grant()`).
    
    The `grant` command returns an object of the following form:
    
        {
            "granted": 1,
            "permissions_changes": [
                {
                    "new_val": { new permissions },
                    "old_val": { original permissions }
                }
            ]
    
    The `granted` field will always be `1`, and the `permissions_changes` list will have one object, describing the new permissions values and the old values they were changed from (which may be `None`).
    
    Permissions that are not defined on a local scope will be inherited from the next largest scope. For example, a write operation on a table will first check if `write` permissions are explicitly set to `True` or `False` for that table and account combination; if they are not, the `write` permissions for the database will be used if those are explicitly set; and if neither table nor database permissions are set for that account, the global `write` permissions for that account will be used.
    
    __Note:__ For all accounts other than the special, system-defined `admin` account, permissions that are not explicitly set in any scope will effectively be `False`. When you create a new user account by inserting a record into the system table, that account will have _no_ permissions until they are explicitly granted.
    
    For a full description of permissions, read Permissions and user accounts.
    
    *Example* Grant the `chatapp` user account read and write permissions on the `users` database.
    
        > r.db(\'users\').grant(\'chatapp\', {\'read\': True, \'write\': True}).run(conn)
        
        {
            "granted": 1,
            "permissions_changes": [
                {
                    "new_val": { "read": true, "write": true },
                    "old_val": { null }
                }
            ]
    
    *Example* Deny write permissions from the `chatapp` account for the `admin` table.
    
        r.db(\'users\').table(\'admin\').grant(\'chatapp\', {\'write\': False}).run(conn)
    
    This will override the `write: true` permissions granted in the first example, but for this table only. Other tables in the `users` database will inherit from the database permissions.
    
    *Example* Delete a table-level permission for the `chatapp` account.
    
        r.db(\'users\').table(\'admin\').grant(\'chatapp\', {\'write\': None}).run(conn)
    
    By specifying `None`, the table scope `write` permission is removed, and will again inherit from the next highest scope (database or global).
    
    *Example* Grant `chatapp` the ability to use HTTP connections.
    
        r.grant(\'chatapp\', {\'connect\': True}).run(conn)
    
    This grant can only be given on a global level.
    
    *Example* Grant a `monitor` account read-only access to all databases.
    
        r.grant(\'monitor\', {\'read\': True}).run(conn)
    '''
def rethinkdb.http()
    '''r.http(url[, options]) -> value
    r.http(url[, options]) -> stream
    
    Retrieve data from the specified URL over HTTP.  The return type depends on the `result_format` option, which checks the `Content-Type` of the response by default.
    
    *Example* Perform an HTTP `GET` and store the result in a table.
    
        r.table(\'posts\').insert(r.http(\'http://httpbin.org/get\')).run(conn)
    
    <!-- stop -->
    
    See [the tutorial](http://rethinkdb.com/docs/external-api-access/) on `r.http` for more examples on how to use this command.
    
    * `timeout`: timeout period in seconds to wait before aborting the connect (default `30`).
    * `attempts`: number of retry attempts to make after failed connections (default `5`).
    * `redirects`: number of redirect and location headers to follow (default `1`).
    * `verify`: if `true`, verify the server\'s SSL certificate (default `true`).
    * `result_format`: string specifying the format to return results in. One of the following:
        * `text`: always return a string.
        * `json`: parse the result as JSON, raising an error on failure.
        * `jsonp`: parse the result as Padded JSON.
        * `binary`: return a binary object.
        * `auto`: parse the result based on its `Content-Type` (the default):
            * `application/json`: as `json`
            * `application/json-p`, `text/json-p`, `text/javascript`: as `jsonp`
            * `audio/*`, `video/*`, `image/*`, `application/octet-stream`: as `binary`
            * anything else: as `text`
    
    * `method`: HTTP method to use for the request. One of `GET`, `POST`, `PUT`, `PATCH`, `DELETE` or `HEAD`. Default: `GET`.
    * `auth`: object giving authentication, with the following fields:
        * `type`: `basic` (default) or `digest`
        * `user`: username
        * `pass`: password in plain text
    * `params`: object specifying URL parameters to append to the URL as encoded key/value pairs. `{ \'query\': \'banana\', \'limit\': 2 }` will be appended as `?query=banana&limit=2`. Default: no parameters.
    * `header`: Extra header lines to include. The value may be an array of strings or an object. Default: `Accept-Encoding: deflate;q=1, gzip;q=0.5` and `User-Agent: RethinkDB/<VERSION>`.
    * `data`: Data to send to the server on a `POST`, `PUT`, `PATCH`, or `DELETE` request. For `POST` requests, data may be either an object (which will be written to the body as form-encoded key/value pairs) or a string; for all other requests, data will be serialized as JSON and placed in the request body, sent as `Content-Type: application/json`. Default: no data will be sent.
    
    *Example* Perform multiple requests with different parameters.
    
        r.expr([1, 2, 3]).map(
            lambda i: r.http(\'http://httpbin.org/get\', params={\'user\': i})
        ).run(conn)
    
    *Example* Perform a `PUT` request for each item in a table.
    
        r.table(\'data\').map(
            lambda row: r.http(\'http://httpbin.org/put\', method=\'PUT\', data=row)
        ).run(conn)
    
    *Example* Perform a `POST` request with accompanying data.
    
    Using form-encoded data:
    
        r.http(\'http://httpbin.org/post\', method=\'POST\',
            data={\'player\': \'Bob\', \'game\': \'tic tac toe\'}
        ).run(conn)
    
    Using JSON data:
    
        r.http(\'http://httpbin.org/post\', method=\'POST\',
            data=r.expr(value).coerce_to(\'string\'),
            header={\'Content-Type\': \'application/json\'}
        ).run(conn)
    
    `r.http` supports depagination, which will request multiple pages in a row and aggregate the results into a stream.  The use of this feature is controlled by the optional arguments `page` and `page_limit`.  Either none or both of these arguments must be provided.
    
    * `page`: This option may specify either a built-in pagination strategy (see below), or a function to provide the next URL and/or `params` to request.
    * `page_limit`: An integer specifying the maximum number of requests to issue using the `page` functionality.  This is to prevent overuse of API quotas, and must be specified with `page`.
        * `-1`: no limit
        * `0`: no requests will be made, an empty stream will be returned
        * `n`: `n` requests will be made
    
    At the moment, the only built-in strategy is `\'link-next\'`, which is equivalent to `lambda info: info\'header\'[\'rel="next"\'].default(None)`.
    
    *Example* Perform a GitHub search and collect up to 3 pages of results.
    
        r.http("https://api.github.com/search/code?q=addClass+user:mozilla",
            page=\'link-next\', page_limit=3).run(conn)
    
    As a function, `page` takes one parameter, an object of the format:
    
        {
            \'params\': object, # the URL parameters used in the last request
            \'header\': object, # the HTTP headers of the last response as key/value pairs
            \'body\': value # the body of the last response in the format specified by `result_format`
        }
    
    The `header` field will be a parsed version of the header with fields lowercased, like so:
    
        {
            \'content-length\': \'1024\',
            \'content-type\': \'application/json\',
            \'date\': \'Thu, 1 Jan 1970 00:00:00 GMT\',
            \'link\': {
                \'rel="last"\': \'http://example.com/?page=34\',
                \'rel="next"\': \'http://example.com/?page=2\'
            }
        }
    
    The `page` function may return a string corresponding to the next URL to request, `None` indicating that there is no more to get, or an object of the format:
    
        {
            \'url\': string, # the next URL to request, or None for no more pages
            \'params\': object # new URL parameters to use, will be merged with the previous request\'s params
        }
    
    *Example* Perform depagination with a custom `page` function.
    
        r.http(\'example.com/pages\',
            page=(lambda info: info[\'body\'][\'meta\'][\'next\'].default(None)),
            page_limit=5
        ).run(conn)
    
    # Learn more
    
    See [the tutorial](http://rethinkdb.com/docs/external-api-access/) on `r.http` for more examples on how to use this command.
    '''
def rethinkdb.iso8601()
    '''r.iso8601(string[, default_timezone=\'\']) -> time
    
    Create a time object based on an ISO 8601 date-time string (e.g. \'2013-01-01T01:01:01+00:00\'). RethinkDB supports all valid ISO 8601 formats except for week dates. Read more about the ISO 8601 format at [Wikipedia](http://en.wikipedia.org/wiki/ISO_8601).
    
    If you pass an ISO 8601 string without a time zone, you must specify the time zone with the `default_timezone` argument.
    
    *Example* Update the time of John\'s birth.
    
        r.table("user").get("John").update({"birth": r.iso8601(\'1986-11-03T08:30:00-07:00\')}).run(conn)
    '''
def rethinkdb.js()
    '''r.js(js_string[, timeout=<number>]) -> value
    
    Create a javascript expression.
    
    *Example* Concatenate two strings using JavaScript.
    
    `timeout` is the number of seconds before `r.js` times out. The default value is 5 seconds.
    
        r.js("\'str1\' + \'str2\'").run(conn)
    
    *Example* Select all documents where the \'magazines\' field is greater than 5 by running JavaScript on the server.
    
        r.table(\'marvel\').filter(
            r.js(\'(function (row) { return row.magazines.length > 5; })\')
        ).run(conn)
    
    *Example* You may also specify a timeout in seconds (defaults to 5).
    
        r.js(\'while(true) {}\', timeout=1.3).run(conn)
    
    '''
def rethinkdb.json()
    '''r.json(json_string) -> value
    
    Parse a JSON string on the server.
    
    *Example* Send an array to the server.
    
        r.json("[1,2,3]").run(conn)
    
    '''
def rethinkdb.line()
    '''r.line([lon1, lat1], [lon2, lat2], ...) -> line
    r.line(point1, point2, ...) -> line
    
    Construct a geometry object of type Line. The line can be specified in one of two ways:
    
    * Two or more two-item arrays, specifying latitude and longitude numbers of the line's vertices;
    * Two or more [Point](http://rethinkdb.com/api/python/point) objects specifying the line's vertices.
    
    <!-- break -->
    
    Longitude (&minus;180 to 180) and latitude (&minus;90 to 90) of vertices are plotted on a perfect sphere. See [Geospatial support](http://rethinkdb.com/docs/geo-support/) for more information on ReQL's coordinate system.
    
    *Example* Define a line.
    
        r.table('geo').insert({
            'id': 101,
            'route': r.line([-122.423246, 37.779388], [-121.886420, 37.329898])
        }).run(conn)
    
    *Example* Define a line using an array of points.
    
    You can use the [args](http://rethinkdb.com/api/python/args) command to pass an array of Point objects (or latitude-longitude pairs) to `line`.
    
        var route = [
            [-122.423246, 37.779388],
            [-121.886420, 37.329898]
        ]
        r.table('geo').insert({
            'id': 102,
            'route': r.line(r.args(route))
        }).run(conn)
    "'''
def rethinkdb.literal()
    '''r.literal(object) -> special
    
    Replace an object in a field instead of merging it with an existing object in a `merge` or `update` operation. = Using `literal` with no arguments in a `merge` or `update` operation will remove the corresponding field.
    
    Assume your users table has this structure:
    
        [
            {
                "id": 1,
                "name": "Alice",
                "data": {
                    "age": 18,
                    "city": "Dallas"
                }
            }       
            ...
        ]
    
    Using `update` to modify the `data` field will normally merge the nested documents:
    
        r.table(\'users\').get(1).update({ \'data\': { \'age\': 19, \'job\': \'Engineer\' } }).run(conn)
        
        {
            "id": 1,
            "name": "Alice",
            "data": {
                "age": 19,
                "city": "Dallas",
                "job": "Engineer"
            }
        }       
    
    That will preserve `city` and other existing fields. But to replace the entire `data` document with a new object, use `literal`.
    
    *Example* Replace one nested document with another rather than merging the fields.
    
        r.table(\'users\').get(1).update({ \'data\': r.literal({ \'age\': 19, \'job\': \'Engineer\' }) }).run(conn)
        
        {
            "id": 1,
            "name": "Alice",
            "data": {
                "age": 19,
                "job": "Engineer"
            }
        }       
    
    *Example* Use `literal` to remove a field from a document.
    
        r.table(\'users\').get(1).merge({ "data": r.literal() }).run(conn)
        
        {
            "id": 1,
            "name": "Alice"
        }
    '''
def rethinkdb.mod()
    '''number % number -> number
    
    Find the remainder when dividing two numbers.
    
    *Example* It's as easy as 2 % 2 = 0.
    
        (r.expr(2) % 2).run(conn)
    
    `
    "'''
def rethinkdb.mul()
    '''number * number -> number
    array * number -> array
    number.mul(number[, number, ...]) -> number
    array.mul(number[, number, ...]) -> array
    
    Multiply two numbers, or make a periodic array.
    
    *Example* It\'s as easy as 2 * 2 = 4.
    
        (r.expr(2) * 2).run(conn)
    
    *Example* Arrays can be multiplied by numbers as well.
    
        (r.expr(["This", "is", "the", "song", "that", "never", "ends."]) * 100).run(conn)
    
    '''
def rethinkdb.net.Connection.close()
    '''conn.close(noreply_wait=True)
    
    Close an open connection.
    
    Closing a connection normally waits until all outstanding requests have finished and then frees any open resources associated with the connection. By passing `False` to the `noreply_wait` optional argument, the connection will be closed immediately, possibly aborting any outstanding noreply writes.
    
    A noreply query is executed by passing the `noreply` option to the [run](http://rethinkdb.com/api/python/run/) command, indicating that `run()` should not wait for the query to complete before returning. You may also explicitly wait for a noreply query to complete by using the [noreply_wait](http://rethinkdb.com/api/python/noreply_wait) command.
    
    *Example* Close an open connection, waiting for noreply writes to finish.
    
        conn.close()
    
    *Example* Close an open connection immediately.
    
        conn.close(noreply_wait=False)
    '''
def rethinkdb.net.Connection.noreply_wait()
    '''conn.noreply_wait()
    
    `noreply_wait` ensures that previous queries with the `noreply` flag have been processed
    by the server. Note that this guarantee only applies to queries run on the given connection.
    
    *Example* We have previously run queries with the `noreply` argument set to `True`. Now
    wait until the server has processed them.
    
        conn.noreply_wait()
    
    '''
def rethinkdb.net.Connection.reconnect()
    '''conn.reconnect(noreply_wait=True)
    
    Close and reopen a connection.
    
    Closing a connection normally waits until all outstanding requests have finished and then frees any open resources associated with the connection. By passing `False` to the `noreply_wait` optional argument, the connection will be closed immediately, possibly aborting any outstanding noreply writes.
    
    A noreply query is executed by passing the `noreply` option to the [run](http://rethinkdb.com/api/python/run/) command, indicating that `run()` should not wait for the query to complete before returning. You may also explicitly wait for a noreply query to complete by using the [noreply_wait](http://rethinkdb.com/api/python/noreply_wait) command.
    
    *Example* Cancel outstanding requests/queries that are no longer needed.
    
        conn.reconnect(noreply_wait=False)
    '''
def rethinkdb.net.Connection.repl()
    '''conn.repl()
    
    Set the default connection to make REPL use easier. Allows calling
    `.run()` on queries without specifying a connection.
    
    __Note:__ Avoid using `repl` in application code. RethinkDB connection objects are not thread-safe, and calls to `connect` from multiple threads may change the global connection object used by `repl`. Applications should specify connections explicitly.
    
    *Example* Set the default connection for the REPL, then call
    `run()` without specifying the connection.
    
        r.connect(db='marvel').repl()
        r.table('heroes').run()
    "'''
def rethinkdb.net.Connection.server()
    '''conn.server()
    
    Return information about the server being used by a connection.
    
    The `server` command returns either two or three fields:
    
    * `id`: the UUID of the server the client is connected to.
    * `proxy`: a boolean indicating whether the server is a RethinkDB proxy node.
    * `name`: the server name. If `proxy` is `True`, this field will not be returned.
    
    *Example* Return server information.
    
        > conn.server()
        
        {
            "id": "404bef53-4b2c-433f-9184-bc3f7bda4a15",
            "name": "amadeus",
            "proxy": False
        }
    '''
def rethinkdb.net.Connection.use()
    '''conn.use(db_name)
    
    Change the default database on this connection.
    
    *Example* Change the default database so that we don't need to
    specify the database when referencing a table.
    
        conn.use('marvel')
        r.table('heroes').run(conn) # refers to r.db('marvel').table('heroes')
    "'''
def rethinkdb.net.Cursor.close()
    '''cursor.close()
    
    Close a cursor. Closing a cursor cancels the corresponding query and frees the memory
    associated with the open request.
    
    *Example* Close a cursor.
    
        cursor.close()
    '''
def rethinkdb.net.Cursor.next()
    '''cursor.next([wait=True])
    
    Get the next element in the cursor.
    
    The optional `wait` argument specifies whether to wait for the next available element and how long to wait:
    
    * `True`: Wait indefinitely (the default).
    * `False`: Do not wait at all. If data is immediately available, it will be returned; if it is not available, a `ReqlTimeoutError` will be raised.
    * number: Wait up to the specified number of seconds for data to be available before raising `ReqlTimeoutError`.
    
    The behavior of `next` will be identical with `False`, `None` or the number `0`.
    
    Calling `next` the first time on a cursor provides the first element of the cursor. If the data set is exhausted (e.g., you have retrieved all the documents in a table), a `ReqlCursorEmpty` error will be raised when `next` is called.
    
    *Example* Retrieve the next element.
    
        cursor = r.table('superheroes').run(conn)
        doc = cursor.next()
    
    *Example* Retrieve the next element on a [changefeed](http://rethinkdb.com/docs/changefeeds/python), waiting up to five seconds.
    
        cursor = r.table('superheroes').changes().run(conn)
        doc = cursor.next(wait=5)
    
    __Note:__ RethinkDB sequences can be iterated through via the Python Iterable interface. The canonical way to retrieve all the results is to use a [for...in](../each/) loop or [list()](../to_array/).
    
    "'''
def rethinkdb.not_()
    '''bool.not_() -> bool
    not_(bool) -> bool
    (~bool) -> bool
    
    Compute the logical inverse (not) of an expression.
    
    `not_` can be called either via method chaining, immediately after an expression that evaluates as a boolean value, or by passing the expression as a parameter to `not_`.  All values that are not `False` or `None` will be converted to `True`.
    
    You may also use `~` as a shorthand operator.
    
    *Example* Not true is false.
    
        r.not_(True).run(conn)
        r.expr(True).not_().run(conn)
        (~r.expr(True)).run(conn)
    
    These evaluate to `false`.
    
    Note that when using `~` the expression is wrapped in parentheses. Without this, Python will evaluate `r.expr(True)` *first* rather than using the ReQL operator and return an incorrect value. (`~True` evaluates to &minus;2 in Python.)
    
    *Example* Return all the users that do not have a "flag" field.
    
        r.table(\'users\').filter(
            lambda users: (~users.has_fields(\'flag\'))
        ).run(conn)
    
    *Example* As above, but prefix-style.
    
        r.table(\'users\').filter(
            lambda users: r.not_(users.has_fields(\'flag\'))
        ).run(conn)
    '''
def rethinkdb.now()
    '''r.now() -> time
    
    Return a time object representing the current time in UTC. The command now() is computed once when the server receives the query, so multiple instances of r.now() will always return the same time inside a query.
    
    *Example* Add a new user with the time at which he subscribed.
    
        r.table("users").insert({
            "name": "John",
            "subscription_date": r.now()
        }).run(conn)
    
    '''
def rethinkdb.object()
    '''r.object([key, value,]...) -> object
    
    Creates an object from a list of key-value pairs, where the keys must
    be strings.  `r.object(A, B, C, D)` is equivalent to
    `r.expr([[A, B], [C, D]]).coerce_to(\'OBJECT\')`.
    
    *Example* Create a simple object.
    
        > r.object(\'id\', 5, \'data\', [\'foo\', \'bar\']).run(conn)
        {\'data\': ["foo", "bar"], \'id\': 5}
    '''
def rethinkdb.or_()
    '''bool | bool -> bool
    bool.or_([bool, bool, ...]) -> bool
    r.or_([bool, bool, ...]) -> bool
    
    Compute the logical "or" of one or more values.
    
    The `or_` command can be used as an infix operator after its first argument (`r.expr(True).or_(False)`) or given all of its arguments as parameters (`r.or_(True, False)`). The standard Python or operator, `|`, may also be used with ReQL.
    
    Calling `or_` with zero arguments will return `False`.
    
    *Example* Return whether either `a` or `b` evaluate to true.
    
        > a = True
        > b = False
        > (r.expr(a) | b).run(conn)
        
        True
    
    *Example* Return whether any of `x`, `y` or `z` evaluate to true.
    
        > x = False
        > y = False
        > z = False
        > r.or_(x, y, z).run(conn)
        
        False
    
    __Note:__ When using `or` inside a `filter` predicate to test the values of fields that may not exist on the documents being tested, you should use the `default` command with those fields so they explicitly return `False`.
    
        r.table(\'posts\').filter(lambda post:
            post[\'category\'].default(\'foo\').eq(\'article\').or(
                post[\'genre\'].default(\'foo\').eq(\'mystery\'))
        ).run(conn)
    '''
def rethinkdb.point()
    '''r.point(longitude, latitude) -> point
    
    Construct a geometry object of type Point. The point is specified by two floating point numbers, the longitude (&minus;180 to 180) and latitude (&minus;90 to 90) of the point on a perfect sphere. See [Geospatial support](http://rethinkdb.com/docs/geo-support/) for more information on ReQL's coordinate system.
    
    *Example* Define a point.
    
        r.table('geo').insert({
            'id': 1,
            'name': 'San Francisco',
            'location': r.point(-122.423246, 37.779388)
        }).run(conn)
    "'''
def rethinkdb.polygon()
    '''r.polygon([lon1, lat1], [lon2, lat2], [lon3, lat3], ...) -> polygon
    r.polygon(point1, point2, point3, ...) -> polygon
    
    Construct a geometry object of type Polygon. The Polygon can be specified in one of two ways:
    
    * Three or more two-item arrays, specifying latitude and longitude numbers of the polygon's vertices;
    * Three or more [Point](http://rethinkdb.com/api/python/point) objects specifying the polygon's vertices.
    
    <!-- break -->
    
    Longitude (&minus;180 to 180) and latitude (&minus;90 to 90) of vertices are plotted on a perfect sphere. See [Geospatial support](http://rethinkdb.com/docs/geo-support/) for more information on ReQL's coordinate system.
    
    If the last point does not specify the same coordinates as the first point, `polygon` will close the polygon by connecting them. You cannot directly construct a polygon with holes in it using `polygon`, but you can use [polygon_sub](http://rethinkdb.com/api/python/polygon_sub) to use a second polygon within the interior of the first to define a hole.
    
    *Example* Define a polygon.
    
        r.table('geo').insert({
            'id': 101,
            'rectangle': r.polygon(
                [-122.423246, 37.779388],
                [-122.423246, 37.329898],
                [-121.886420, 37.329898],
                [-121.886420, 37.779388]
            )
        }).run(conn)
    
    *Example* Define a polygon using an array of vertices.
    
    You can use the [args](http://rethinkdb.com/api/python/args) command to pass an array of Point objects (or latitude-longitude pairs) to `polygon`.
    
        vertices = [
            [-122.423246, 37.779388],
            [-122.423246, 37.329898],
            [-121.886420, 37.329898],
            [-121.886420, 37.779388]
        ]
        r.table('geo').insert({
            'id': 102,
            'rectangle': r.polygon(r.args(vertices))
        }).run(conn)
    "'''
def rethinkdb.random()
    '''r.random() -> number
    r.random(number[, number], float=True) -> number
    r.random(integer[, integer]) -> integer
    
    Generate a random number between given (or implied) bounds. `random` takes zero, one or two arguments.
    
    - With __zero__ arguments, the result will be a floating-point number in the range `[0,1)` (from 0 up to but not including 1).
    - With __one__ argument _x,_ the result will be in the range `[0,x)`, and will be integer unless `float=True` is given as an option. Specifying a floating point number without the `float` option will raise an error.
    - With __two__ arguments _x_ and _y,_ the result will be in the range `[x,y)`, and will be integer unless `float=True` is given as an option.  If _x_ and _y_ are equal an error will occur, unless the floating-point option has been specified, in which case _x_ will be returned. Specifying a floating point number without the `float` option will raise an error.
    
    Note: The last argument given will always be the 'open' side of the range, but when
    generating a floating-point number, the 'open' side may be less than the 'closed' side.
    
    *Example* Generate a random number in the range `[0,1)`
    
        r.random().run(conn)
    
    *Example* Generate a random integer in the range `[0,100)`
    
        r.random(100).run(conn)
        r.random(0, 100).run(conn)
    
    *Example* Generate a random number in the range `(-2.24,1.59]`
    
        r.random(1.59, -2.24, float=True).run(conn)
    
    "'''
def rethinkdb.range()
    '''r.range() -> stream
    r.range([start_value, ]end_value) -> stream
    
    Generate a stream of sequential integers in a specified range.
    
    `range` takes 0, 1 or 2 arguments:
    
    * With no arguments, `range` returns an "infinite" stream from 0 up to and including the maximum integer value;
    * With one argument, `range` returns a stream from 0 up to but not including the end value;
    * With two arguments, `range` returns a stream from the start value up to but not including the end value.
    
    Note that the left bound (including the implied left bound of 0 in the 0- and 1-argument form) is always closed and the right bound is always open: the start value will always be included in the returned range and the end value will *not* be included in the returned range.
    
    Any specified arguments must be integers, or a `ReqlRuntimeError` will be thrown. If the start value is equal or to higher than the end value, no error will be thrown but a zero-element stream will be returned.
    
    *Example* Return a four-element range of `[0, 1, 2, 3]`.
    
        > r.range(4).run(conn)
        
        [0, 1, 2, 3]
    
    <!-- stop -->
    
    You can also use the [limit](http://rethinkdb.com/api/python/limit) command with the no-argument variant to achieve the same result in this case:
    
        > r.range().limit(4).run(conn)
        
        [0, 1, 2, 3]
    
    *Example* Return a range from -5 through 5.
    
        > r.range(-5, 6).run(conn)
        
        [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    '''
def rethinkdb.row()
    '''r.row -> value
    
    Returns the currently visited document.
    
    *Example* Get all users whose age is greater than 5.
    
        r.table('users').filter(r.row['age'] > 5).run(conn)
    
    *Example* Access the attribute 'child' of an embedded document.
    
        r.table('users').filter(r.row['embedded_doc']['child'] > 5).run(conn)
    
    *Example* Add 1 to every element of an array.
    
        r.expr([1, 2, 3]).map(r.row + 1).run(conn)
    
    *Example* For nested queries, use functions instead of `row`.
    
        r.table('users').filter(
            lambda doc: doc['name'] == r.table('prizes').get('winner')
        ).run(conn)
    
    "'''
def rethinkdb.set_loop_type()
    '''r.set_loop_type(string)
    
    Set an asynchronous event loop model. There are two supported models:
    
    * `"tornado"`: use the Tornado web framework. Under this model, the connect and run commands will return Tornado `Future` objects.
    * `"twisted"`: use the Twisted networking engine. Under this model, the connect and run commands will return Twisted `Deferred` objects.
    
    *Example* Read a table\'s data using Tornado.
    
        r.set_loop_type("tornado")
        conn = r.connect(host=\'localhost\', port=28015)
        
        @gen.coroutine
        def use_cursor(conn):
            # Print every row in the table.
            cursor = yield r.table(\'test\').order_by(index="id").run(yield conn)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                print(item)
    
    For a longer discussion with both Tornado and Twisted examples, see the documentation article on Asynchronous connections.
    
    '''
def rethinkdb.sub()
    '''number - number -> number
    time - number -> time
    time - time -> number
    number.sub(number[, number, ...]) -> number
    time.sub(number[, number, ...]) -> time
    time.sub(time) -> number
    
    Subtract two numbers.
    
    *Example* It's as easy as 2 - 2 = 0.
    
        (r.expr(2) - 2).run(conn)
    
    *Example* Create a date one year ago today.
    
        r.now() - 365*24*60*60
    
    *Example* Retrieve how many seconds elapsed between today and `date`.
    
        r.now() - date
    
    "'''
def rethinkdb.time()
    '''r.time(year, month, day[, hour, minute, second], timezone)
        -> time
    
    Create a time object for a specific time.
    
    A few restrictions exist on the arguments:
    
    - `year` is an integer between 1400 and 9,999.
    - `month` is an integer between 1 and 12.
    - `day` is an integer between 1 and 31.
    - `hour` is an integer.
    - `minutes` is an integer.
    - `seconds` is a double. Its value will be rounded to three decimal places
    (millisecond-precision).
    - `timezone` can be `\'Z\'` (for UTC) or a string with the format `\xc2\xb1[hh]:[mm]`.
    
    *Example* Update the birthdate of the user "John" to November 3rd, 1986 UTC.
    
        r.table("user").get("John").update({"birthdate": r.time(1986, 11, 3, \'Z\')}).run(conn)
    
    '''
def rethinkdb.uuid()
    '''r.uuid([string]) -> string
    
    Return a UUID (universally unique identifier), a string that can be used as a unique ID. If a string is passed to `uuid` as an argument, the UUID will be deterministic, derived from the string\'s SHA-1 hash.
    
    RethinkDB\'s UUIDs are standards-compliant. Without the optional argument, a version 4 random UUID will be generated; with that argument, a version 5 UUID will be generated, using a fixed namespace UUID of `91461c99-f89d-49d2-af96-d8e2e14e9b58`. For more information, read Wikipedia\'s UUID article.
    
    *Example* Generate a UUID.
    
        > r.uuid().run(conn)
        
        "27961a0e-f4e8-4eb3-bf95-c5203e1d87b9"
    
    *Example* Generate a UUID based on a string.
    
        > r.uuid("slava@example.com").run(conn)
        
        "90691cbc-b5ea-5826-ae98-951e30fc3b2d"
    '''