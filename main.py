import datetime
from connect import connect
from send2 import send

# get today's datetime
today = datetime.datetime.today()


# hard-coded email contacts given matter_type and handling_firm
contacts_247 = {
    'paraquat' : {'motley rice' : ['rwindsor@motleyrice.com', 'cscott@motleyrice.com', 'ffitzpatrick@motleyrice.com']},
    'rideshare' : {'nachawati law group' : ['dbias@ntrial.com', 'lroundtree@ntrial.com']},
    'talc' : {'ashcraft & gerel' : ['plyons@ashcraftlaw.com']},
    'talc workup' : {'ashcraft & gerel' : ['plyons@ashcraftlaw.com']},
    'afff' : {'elg' : ['treven@elglaw.com'], 'susen law group' : ['nsimet@hirecsg.com']},
    'afff workup' : {'elg' : ['treven@elglaw.com'], 'susen law group' : ['nsimet@hirecsg.com']},
    'roundup' : {'kline & specter' : ['priscilla.jimenez@klinespecter.com', 'madisyn.zadjeika@klinespecter.com']},
    'hair straightener' : {'ashcraft & gerel' : ['plyons@ashcraftlaw.com']},
    'camp lejeune' : {'krause & kinsman' : ['adam@krauseandkinsman.com', 'bryan@krauseandkinsman.com', 'schery@krauseandkinsman.com'],
                      'wright & schulte' : ['ryan@ibexlegal.com', 'greg@ibexlegal.com']},
    'hernia mesh' : {'wright & schulte' : ['ryan@ibexlegal.com', 'greg@ibexlegal.com']},
    'truvada' : {'parafinczuk wolf' : ['nnelson@parawolf.com']},
    'toxic metal baby formula' : {'wagstaff' : ['hcharm@wagstafflawfirm.com']},
}

contacts_252 = {
    'roundup': {'kline & specter' : ['madisyn.zadjeika@klinespecter.com']},
    'talc': {'ashcraft & gerel' : ['plyons@ashcraftlaw.com']},
    'talc workup' : {'ashcraft & gerel' : ['plyons@ashcraftlaw.com']},
    'hair straightener' : {'ashcraft & gerel' : ['plyons@ashcraftlaw.com']}
}
##############################################################################
# Test
# contacts_247 = {
#     'paraquat' : {'motley rice' : ['737791989@qq.com']},
#     'rideshare' : {'nachawati law group' : ['737791989@qq.com']},
#     'talc' : {'ashcraft & gerel' : ['737791989@qq.com']},
#     'afff' : {'elg' : ['737791989@qq.com']},
#     'roundup' : {'kline & spector' : ['737791989@qq.com']},
#     'hair straightener' : {'ashcraft & gerel' : ['737791989@qq.com']},
#     'camp lejeune' : {'krause & kinsman' : ['737791989@qq.com'],
#                       'wright & schulte' : ['737791989@qq.com']},
#     'hernia mesh' : {'wright & schulte' : ['737791989@qq.com']},
#     'truvada' : {'parafinczuk wolf' : ['737791989@qq.com']},
#     'apap' : {'susen law group' : ['737791989@qq.com']},
#     'toxic metal baby formula' : {'wagstaff' : ['737791989@qq.com', 'xxhgoodluck@gmail.com']},
# }

# contacts_252 = {
#     'roundup': {'kline & spector' : ['737791989@qq.com', 'xxhgoodluck@gmail.com']},
#     'talc': {'ashcraft & gerel' : ['xuhanxie@outlook.com']},
#     'hair straightener' : {'ashcraft & gerel' : ['xuhanxie@outlook.com']}
# }
##################################################################################

def main():
    # connect to database
    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()
        # execute sql query statement
        sql_query = "SELECT matter_type, MAX(ext.last_upload_time) AS latest_upload_time, `litt_o`.`target_org_alias` AS `handing_firm_name`, m.organization_id AS orgID FROM bl_venture_matter.bl_matter m LEFT JOIN bl_venture_matter.bl_matter_ext ext ON ext.matter_id = m.matter_id LEFT JOIN `bl_venture_matter`.`bl_matter_relation_org` `litt` ON `litt`.`matter_id` = `m`.`matter_id` AND `litt`.`org_relation_id` = 3 AND `litt`.archive = 0 LEFT JOIN `bl_venture_config`.`bl_lead_type_relation_org` `litt_o` ON `litt_o`.`target_org_id` = `litt`.`organization_id` AND `litt_o`.`organization_id` = `m`.`organization_id` AND `litt_o`.`archive` = 0 WHERE m.organization_id IN (247, 252) AND m.archive = 0 AND ext.last_upload_time IS NOT NULL AND `litt_o`.`target_org_alias` IS NOT NULL GROUP BY matter_type, `litt_o`.`target_org_alias`, m.organization_id HAVING DATEDIFF(CURDATE(), latest_upload_time) > 15 ORDER BY m.organization_id, matter_type;"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        print("database result retrieved")
        print(result)
        print("sending emails...")
        email_list = {} # For testing
        for row in result:
            # maintain the consistency between data retrieve from database and contacts map
            matter_type = row[0].lower()
            handling_firm = row[2].lower()
            org_id = row[3]
            # notification should be made
            receiver_emails = []
            if org_id == 247:
                if matter_type in contacts_247 and handling_firm in contacts_247[matter_type]:
                    receiver_emails = contacts_247[matter_type][handling_firm]
            elif org_id == 252:
                if matter_type in contacts_252 and handling_firm in contacts_252[matter_type]:
                    receiver_emails = contacts_252[matter_type][handling_firm]
            # send emails, make sure to use the code line 85 to 90 to confirm the email list selected is correct.
            if len(receiver_emails) > 0:
                send(matter_type=matter_type, email_list=receiver_emails, org_id=org_id)
        # the code below is just testing the receiver emails selected, before actually sent the emails.
            
            if len(receiver_emails) > 0:
                if matter_type not in email_list:
                    email_list[matter_type] = []
                email_list[matter_type].append(receiver_emails)
        print(email_list)
        print("completed")
    except Exception as e:
        print(e)

    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")

if __name__ == '__main__':
    main()