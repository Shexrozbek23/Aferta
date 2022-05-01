
# import datetime
def calculation(service_type,square_of_services):

    if service_type>=1 and service_type<=43 and square_of_services>0:
        if service_type>=1 and service_type<=5:
            if square_of_services>0 and square_of_services<=50:
                summa=square_of_services*55240
                return summa
            elif square_of_services>50 and square_of_services<=100:
                summa=square_of_services*47600
                return summa
            elif square_of_services>100 and square_of_services<=500:
                summa=square_of_services*32800
                return summa
            elif square_of_services>500 and square_of_services<=1000:
                summa=square_of_services*25300
                return summa
            elif square_of_services>1000:
                summa=square_of_services*20450
                return summa
        elif service_type==6:
            summa=square_of_services*23250
            return summa
        elif service_type==7:
            summa=square_of_services*16300
            return summa
        elif service_type==8:
            summa=square_of_services*19000
            return summa
        elif service_type==9:
            summa=square_of_services*14100
            return summa
        elif service_type==10:
            summa=square_of_services*25000
            return summa
        elif service_type==11:
            summa=square_of_services*100000
            return summa
        elif service_type==12:
            summa=square_of_services*20400
            return summa
        elif service_type==13:
            summa=square_of_services*38600
            return summa
        elif service_type==14:
            summa=square_of_services*26700
            return summa
        elif service_type==15:
            summa=square_of_services*19500
            return summa
        elif service_type==16:
            summa=square_of_services*26400
            return summa
        elif service_type==17:
            summa=square_of_services*25900
            return summa
        elif service_type==18:
            summa=square_of_services*26400
            return summa
        elif service_type==19:
            summa=square_of_services*20300
            return summa
        elif service_type==20:
            summa=square_of_services*32000
            return summa
        elif service_type==21:
            summa=square_of_services*26300
        elif service_type==22:
            summa=square_of_services*29200
            return summa
        elif service_type==23:
            summa=square_of_services*29200
            return summa
        elif service_type==24:
            summa=square_of_services*29200
            return summa
        elif service_type==25:
            summa=square_of_services*27700
            return summa
        elif service_type==26:
            summa=square_of_services*79100
            return summa
        elif service_type==27:
            summa=square_of_services*29200
            return summa
        elif service_type==28:
            summa=square_of_services*146000
            return summa
        elif service_type==29:
            summa=square_of_services*176500
            return summa
        elif service_type==30:
            summa=square_of_services*178500
            return summa
        elif service_type==31:
            summa=square_of_services*29200
            return summa
        elif service_type==32:
            summa=square_of_services*29200
            return summa
        elif service_type==33:
            summa=square_of_services*51000
            return summa
        elif service_type==34:
            summa=square_of_services*113400
            return summa
        elif service_type==35:
            summa=square_of_services*615100
            return summa
        elif service_type==36:
            summa=square_of_services*436200
            return summa
        elif service_type==37:
            summa=square_of_services*57300
            return summa
        elif service_type==38:
            summa=square_of_services*279000
            return summa
        elif service_type==39:
            summa=square_of_services*400000
            return summa
        elif service_type==40:
            summa=square_of_services*455000
            return summa
        elif service_type==41:
            summa=square_of_services*408700
            return summa
        elif service_type==42:
            summa=square_of_services*478000
            return summa
        elif service_type==43:
            summa=square_of_services*407000
            return summa
        else:
            summa= False
            
    else:
        
        summa= False
        return summa

# def generete(region_pk,service_type):
#     current_year = int(datetime.datetime.now().strftime('%y'))
#     if int(region_pk) < 10:
#         first_four_digits = str(current_year) + '0' + str(region_pk)
#     else:
#         first_four_digits = str(current_year) + str(region_pk)

#     if int(service_type) < 10:
#         first_six_digits = str(first_four_digits) + '0' + str(service_type)
#     else:
#         first_six_digits = str(first_four_digits) + str(service_type)

#     last_invoice = False
#     if last_invoice:
#         invoice_number = int(last_invoice.number) + 1
#     else:
#         invoice_number = int(first_six_digits) * 100000 + 1
#     return invoice_number
