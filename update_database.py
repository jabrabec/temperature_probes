def update_database():
    '''
    Connect to mongoDB, get the current readings from read_probes function,
    update db with these results, and confirm successful save of new readings.
    '''

    from read_probes import read_probes
    from pymongo import MongoClient

    client = MongoClient()

    # mongoDB db name is 'temp_probes'
    db = client.temp_probes

    # Collect the current readings from probes and store in 'result'
    result = read_probes()

    # mongoDB collection in 'temp_probes' db is 'readings'.
    # Add these results to db using insert_one command.
    items_to_add = db.readings.insert_many(result)

    # If insert_one was successful, mongoDB will have generated an inserted_id
    # value. Check that this value exists and return True for function if so.
    # Otherwise, function returns None.
    if items_to_add.inserted_ids:
        return True


if __name__ == "__main__":

    # Attempt to update the database when this file is run directly.
    # Print successful db insertion message if update_database returns True.
    if update_database():
        print "Saved new readings to db."
    # Otherwise indicate failure to update db.
    else:
        print "Failed to save new readings to db."
