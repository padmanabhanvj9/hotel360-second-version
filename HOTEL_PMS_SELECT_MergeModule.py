from sqlwrapper import gensql, dbget,dbput
import json
import datetime

date = json.loads(dbget("select roll_business_date from endofday.business_date"))
print(date)
next_day = (datetime.datetime.strptime(date[0]['roll_business_date'],'%Y-%m-%d').date()) + datetime.timedelta(days=1)
yesterday_date = (datetime.datetime.strptime(date[0]['roll_business_date'],'%Y-%m-%d').date()) - datetime.timedelta(days=1)

    
#todays_date = datetime.datetime.utcnow().date()
def Hotel_PMS_Select_GetTodayRoomAvailabilityArrival(request):
    
    final = []
   
    sql = json.loads(dbget("SELECT 'checkin' as dash_board ,COUNT(*) FROM reservation.res_reservation WHERE res_guest_status='checkin' and res_arrival='"+str(date[0]['roll_business_date'])+"' \
                            union \
                            SELECT 'checkout' , COUNT(*) FROM reservation.res_reservation WHERE res_guest_status='Check out' and res_depature='"+str(date[0]['roll_business_date'])+"' \
                            union \
                            SELECT 'arrival' ,COUNT(*) FROM reservation.res_reservation WHERE res_guest_status ='arrival' and res_arrival='"+str(date[0]['roll_business_date'])+"' \
                            union \
                            select 'due_out' , count(*) from reservation.res_reservation where res_guest_status='due out' and  res_depature ='"+str(next_day)+"' \
                            union \
                            select 'reservation' ,count(*) from reservation.res_reservation where created_on='"+str(date[0]['roll_business_date'])+"' \
                            union  \
                            select 'room_availability' ,count(*) from room_management.rm_room_list where rm_reservation_status='not reserved'  "))
    print(sql)
   
   
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','ReturnValue':sql,'ReturnCode':'RRTS'},indent=4))

def Hotel_PMS_cancel_DepositRuleReservation(request):
    RES_Log_Time = datetime.datetime.utcnow()+datetime.timedelta(hours=5, minutes=30)
    RES_Log_Time = RES_Log_Time.time().strftime("%H:%M:%S")
    sql = json.loads(dbget("select res_id from reservation.res_deposit \
                            where res_due_date = '"+str(yesterday_date)+"'"))
    
    for i in sql:
        
        psql = dbput("update reservation.res_reservation set res_guest_status = 'cancel' \
                     where res_id = '"+str(i['res_id'])+"'")
        print(psql)
        select = json.loads(dbget("select * from reservation.cancel_id"))
        print(select,type(select),len(select))
        print(select[0]['id'])
        cancel_id = str(select[0]['id']+1)
        print(cancel_id)
        update = dbput("update reservation.cancel_id set id = '"+str(select[0]['id']+1)+"'")
        s = {}
        s['Emp_Id'] = '121'
        s['Emp_Firstname'] = 'Ranimangama'
       
        s['RES_Log_Date'] = datetime.datetime.utcnow().date()
        s['RES_Log_Time'] = RES_Log_Time
        s['RES_Action_Type'] = "Cancel Reservation"
        s['RES_Description'] = "cancellation Number is" +" "+ cancel_id
        s['Res_id'] = i['res_id']
        
        sql_value = gensql('insert','reservation.res_activity_log',s)
    return(json.dumps({'Status': 'Success', 'StatusCode': '200','Return': 'Record Updated Successfully','ReturnCode':'RUS'}, sort_keys=True, indent=4))
    

