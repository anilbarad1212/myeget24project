from ast import Return
from pickle import TRUE
from unicodedata import category
from django.shortcuts import redirect, render
from mobiles.models import All_Accesories, All_Brands, All_Mobiles, Cart, CustomUser, CustomerAddress, OrderPlaced, Payment, Return_Order
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CodeForm, CustomerRegistrationForm, LoginForm, Change_Mobile_Number_Form
from otp.models import Code
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt
from .utils import genret_order_id, sent_order_confirmation_mesaage
import mobiles.Checksum as Checksum
import datetime
from django.http import HttpResponse
from django.db import transaction
import random
from dateutil.parser import parse
from django.contrib.auth.decorators import login_required

MERCHANT_KEY = 'RX0hpjvtTBiXZleF'

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'mobiles/login.html', {'form': form})


def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = CustomUser.objects.get(pk=pk)
        user_id = user.id
        otp = user.code.otp
        user_otp = f"{user.username} : {user.code.otp}"
        if not request.POST:
            # send_sms(user_otp, user.phone_number)
            print('hello')
        if form.is_valid():
            digits = form.cleaned_data.get('number')
            if str(otp) == str(digits):
                new_user = CustomUser.objects.get(pk=pk)
                delete_data = Code.objects.get(
                    otp=digits,
                    user=new_user,
                ).delete()
                new_otp = random.randint(1, 1000)
                user_new_otp = Code.objects.create(otp=str(new_otp),
                                                   user=new_user)
                messages.success(
                    request,
                    'Congratulations!! Phone Number Verified Successfully')
                return redirect('login')
            else:
                messages.success(request, 'OTP didnt matched')
    return render(request, 'mobiles/otp.html', {'form': form})


def register(request):
    print('REGISTRATION')
    form = CustomerRegistrationForm(request.POST or None)
    print('FORM', form)

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']

            password = form.cleaned_data['password1']

            password_two = form.cleaned_data['password2']

            email = form.cleaned_data['email']

            phone_num = form.cleaned_data['phone_number']

            check_phone_number = CustomUser.objects.filter(
                phone_number=phone_num).first()
            if check_phone_number:
                messages.success(request, 'Phone Number Already Registered')
            check_email_address = CustomUser.objects.filter(
                email=email).first()
            if check_email_address:
                messages.success(request, 'Email Already Registered')

            else:
                messages.success(
                    request,
                    'Congratulations!! Account Reggisterd Successfully')
                reg_user = form.save()
                user = CustomUser.objects.get(username=username,
                                              phone_number=phone_num)
                if user is not None:
                    request.session['pk'] = user.pk
                    return redirect('verify')
    return render(request, 'mobiles/register.html', {'form': form})


def change_phone_number(request):
    pk = request.session.get('pk')
    # user = CustomUser.objects.get(pk=pk)
    # print('USER IN SIDE PHONE NUMBER',user)
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=pk)
        print('USER INSIDE PHONE NUMBER', user)
        form = Change_Mobile_Number_Form(request.POST, instance=user)
        print(form, 'form')
        if form.is_valid():
            form.save()
            request.session['pk'] = user.pk
            return redirect('verify')
    else:
        user = CustomUser.objects.get(pk=pk)
        print(user.id)
        form = Change_Mobile_Number_Form(instance=user)
        # request.session['pk'] = user.pk
        # return redirect('verify')
    return render(request, 'mobiles/change-number.html', {'form': form})


def home(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    trending_deals = All_Accesories.objects.filter(sub_category='TP')
    all_brand_photos = All_Brands.objects.all()
    return render(
        request, 'mobiles/home.html', {
            'total_item': total_item,
            'trending_deals': trending_deals,
            'all_brand_photos': all_brand_photos
        })


def all_mobiles(request, data):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    mobiles = All_Mobiles.objects.filter(all_brands__brand_name=data)
    return render(request, 'mobiles/all_mobiles.html', {
        'mobiles': mobiles,
        'data': data,
        'total_item': total_item
    })


def accesories_view(request, id):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    mobile = All_Mobiles.objects.get(id=id)
    back_pannel_cover = All_Accesories.objects.filter(all_mobiles=mobile,
                                                      category='BCK-PNEL-CVR')
    print('backpannelcover', back_pannel_cover)
    print()
    bettry_connector = All_Accesories.objects.filter(all_mobiles=mobile,
                                                     category='BTR-CNCTR')
    print('bettry connector', bettry_connector)
    print()
    bettries = All_Accesories.objects.filter(all_mobiles=mobile,
                                             category='BTR')
    print('bettries', bettries)
    print()
    camera_lense = All_Accesories.objects.filter(all_mobiles=mobile,
                                                 category='CMR-LNS')
    charging_conctr = All_Accesories.objects.filter(all_mobiles=mobile,
                                                    category='CHRG-CNTR')
    charging_pcb = All_Accesories.objects.filter(all_mobiles=mobile,
                                                 category='CHRG-PCB')
    ear_spker = All_Accesories.objects.filter(all_mobiles=mobile,
                                              category='EAR-SPK')
    fingpr_sensor_flx_cable = All_Accesories.objects.filter(
        all_mobiles=mobile, category='FNGP-SN-FLX-CB')
    finger_snsr_btn_plsatic = All_Accesories.objects.filter(
        all_mobiles=mobile, category='FNGP-SN-BTN-PLST')
    fullbodY_hosing = All_Accesories.objects.filter(all_mobiles=mobile,
                                                    category='FLBD-HOU')
    handsfre_jack = All_Accesories.objects.filter(all_mobiles=mobile,
                                                  category='HNDFR-JK')
    lcd_conectr = All_Accesories.objects.filter(all_mobiles=mobile,
                                                category='LCD-CONT')
    lcd_flx = All_Accesories.objects.filter(all_mobiles=mobile,
                                            category='LCD-FLX')
    lcd_frm_midl_chasis = All_Accesories.objects.filter(
        all_mobiles=mobile, category='LCD-FRM-MDL-CH')
    loud_spkr_ringr = All_Accesories.objects.filter(all_mobiles=mobile,
                                                    category='LUD-SPK-RIG')
    main_brd_flx_cbl = All_Accesories.objects.filter(all_mobiles=mobile,
                                                     category='MN-BD-FLX-CB')
    mmc_conectr = All_Accesories.objects.filter(all_mobiles=mobile,
                                                category='MC-CONT')
    powr_btn_flx_cable = All_Accesories.objects.filter(
        all_mobiles=mobile, category='PWR-BTN-FLX-CB')
    volume_btn_flx_cable = All_Accesories.objects.filter(
        all_mobiles=mobile, category='VLM-BTN-FLX-CB')
    power_btn_otr_plstic = All_Accesories.objects.filter(
        all_mobiles=mobile, category='PWR-BTN-OTR-PLS')
    back_camera = All_Accesories.objects.filter(all_mobiles=mobile,
                                                category='BK-CMR')
    frnt_cmr_slfi = All_Accesories.objects.filter(all_mobiles=mobile,
                                                  category='FRT-CMR-SLF')
    front_mn_glass = All_Accesories.objects.filter(all_mobiles=mobile,
                                                   category='FRT-MN-GLS')
    front_mn_touch = All_Accesories.objects.filter(all_mobiles=mobile,
                                                   category='FRT-MN-TC')
    simcrd_holdr_try = All_Accesories.objects.filter(all_mobiles=mobile,
                                                     category='SIM-HLD-TRY')
    sim_conctr = All_Accesories.objects.filter(all_mobiles=mobile,
                                               category='SIM-CONT')
    spker_jali = All_Accesories.objects.filter(all_mobiles=mobile,
                                               category='SPKR-JL')
    vibrators = All_Accesories.objects.filter(all_mobiles=mobile,
                                              category='VBR')
    volume_btn_plstc = All_Accesories.objects.filter(all_mobiles=mobile,
                                                     category='VLM-BTN-PLS')
    antena_ntwrk_wire = All_Accesories.objects.filter(all_mobiles=mobile,
                                                      category='ANTN-NET-WR')
    flip_cover = All_Accesories.objects.filter(all_mobiles=mobile,
                                               category='FLP-CVR')
    return render(
        request, 'mobiles/parts.html', {
            'mobile': mobile,
            'back_pannel_cover': back_pannel_cover,
            'bettry_connector': bettry_connector,
            'bettries': bettries,
            'camera_lense': camera_lense,
            'charging_conctr': charging_conctr,
            'charging_pcb': charging_pcb,
            'ear_spker': ear_spker,
            'fingpr_sensor_flx_cable': fingpr_sensor_flx_cable,
            'finger_snsr_btn_plsatic': finger_snsr_btn_plsatic,
            'fullbodY_hosing': fullbodY_hosing,
            'handsfre_jack': handsfre_jack,
            'lcd_conectr': lcd_conectr,
            'lcd_flx ': lcd_flx,
            'lcd_frm_midl_chasis': lcd_frm_midl_chasis,
            'loud_spkr_ringr': loud_spkr_ringr,
            'main_brd_flx_cbl': main_brd_flx_cbl,
            'mmc_conectr': mmc_conectr,
            'powr_btn_flx_cable': powr_btn_flx_cable,
            'volume_btn_flx_cable': volume_btn_flx_cable,
            'power_btn_otr_plstic': power_btn_otr_plstic,
            'back_camera': back_camera,
            'frnt_cmr_slfi': frnt_cmr_slfi,
            'front_mn_glass': front_mn_glass,
            'front_mn_touch': front_mn_touch,
            'simcrd_holdr_try': simcrd_holdr_try,
            'sim_conctr': sim_conctr,
            'spker_jali': spker_jali,
            'vibrators': vibrators,
            'volume_btn_plstc': volume_btn_plstc,
            'antena_ntwrk_wire': antena_ntwrk_wire,
            'flip_cover': flip_cover,
            'total_item': total_item
        })


def product_detail(request, id):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    product = All_Accesories.objects.get(id=id)
    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(
            Q(all_accesories=product.id) & Q(user=request.user)).exists()
    tday = datetime.date.today()
    tdelta = datetime.timedelta(days=2)
    date = tday + tdelta
    month = date.strftime("%B")
    weekday = date.strftime("%A")
    date = date.day

    return render(
        request, 'mobiles/productdetail.html', {
            'product': product,
            'month': month,
            'date': date,
            'weekday': weekday,
            'item_already_in_cart': item_already_in_cart,
            'total_item': total_item
        })


def add_to_cart(request):
    user = request.user
    product = request.GET.get('prod_id')
    product_id = All_Accesories.objects.get(id=product)
    all_ready_cart = Cart.objects.filter(user=user, all_accesories=product_id)
    if all_ready_cart:
        print('all ready cart', all_ready_cart)
        all_ready_cart.delete()
    cart_items = Cart.objects.create(user=user, all_accesories=product_id)
    print('cart item', cart_items)
    cart_items.save()
    return redirect('/cart')


def show_cart(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for users_cart in cart_product:
                tempamount = (users_cart.quantity *
                              users_cart.all_accesories.price)
                total_amount = total_amount + tempamount

            tday = datetime.date.today()
            tdelta = datetime.timedelta(days=2)
            date = tday + tdelta
            month = date.strftime("%B")
            years = date.strftime("%Y")
            weekday = date.strftime("%A")
            date = date.strftime("%d")
            expected_delivery_date = weekday + '    , ' + date + ' ' + month + ' ' + years
            return render(
                request, 'mobiles/addtocart.html', {
                    'carts': cart,
                    'total_amount': total_amount,
                    'expected_delivery_date': expected_delivery_date,
                    'total_item': total_item
                })
        else:
            return render(request, 'mobiles/empty-cart.html')


def plus_cart(request):
    if request.method == 'GET':
        prodd_id = request.GET['prodd_id']
        accesories_id = All_Accesories.objects.get(id=prodd_id)
        c = Cart.objects.get(
            Q(all_accesories=accesories_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        total_amount = 0.0
        cart_product = [
            p for p in Cart.objects.all() if p.user == request.user
        ]
        for users_cart in cart_product:
            tempamount = (users_cart.quantity *
                          users_cart.all_accesories.price)
            total_amount = total_amount + tempamount
        data = {
            'quantity': c.quantity,
            'amount': total_amount,
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        proddd_id = request.GET['proddd_id']
        accesories_id = All_Accesories.objects.get(id=proddd_id)
        c = Cart.objects.get(
            Q(all_accesories=accesories_id) & Q(user=request.user))
        c.quantity -= 1
        if c.quantity == 0:
            c.quantity += 1
        c.save()
        amount = 0.0
        total_amount = 0.0
        cart_product = [
            p for p in Cart.objects.all() if p.user == request.user
        ]
        for users_cart in cart_product:
            tempamount = (users_cart.quantity *
                          users_cart.all_accesories.price)
            total_amount = total_amount + tempamount
        data = {
            'quantity': c.quantity,
            'amount': total_amount,
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prodc_id = request.GET['prodc_id']
        accesories_id = All_Accesories.objects.get(id=prodc_id)
        c = Cart.objects.get(
            Q(all_accesories=accesories_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        total_amount = 0.0
        cart_product = [
            p for p in Cart.objects.all() if p.user == request.user
        ]
        for users_cart in cart_product:
            tempamount = (users_cart.quantity *
                          users_cart.all_accesories.price)
            total_amount = total_amount + tempamount
        data = {
            'amount': total_amount,
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'mobiles/buynow.html')


def profileView(request):
    order_id = genret_order_id()
    if request.method == 'POST':
        user = request.user
        total_amount = request.POST.get('amount')
        print(total_amount, 'total amount')
        print(total_amount, 'total cost')
        email = request.POST.get('email')
        adddress_one = request.POST.get('address1')
        address_two = request.POST.get('address2')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pin')
        mobile_number = request.POST.get('phone')
        order_id = genret_order_id()
        reg = CustomerAddress.objects.create(order_number=order_id,
                                             user=user,
                                             email=email,
                                             address1=adddress_one,
                                             address2=address_two,
                                             landmark=landmark,
                                             city=city,
                                             state=state,
                                             pincode=pincode,
                                             mobile_number=mobile_number)
        reg.save()
        messages.success(
            request,
            'Congratulations !! Your Address Has Been Updated Successfully')

        tday = datetime.date.today()
        tdelta = datetime.timedelta(days=2)
        date = tday + tdelta
        month = date.strftime("%B")
        years = date.strftime("%Y")
        weekday = date.strftime("%A")
        date = date.strftime("%d")
        expected_delivery_date = weekday + ' ' + date + ' ' + month + ' ' + years

        customer_addrs = CustomerAddress.objects.get(id=reg.id)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced.objects.create(
                order_number=order_id,
                user=user,
                customer_address=customer_addrs,
                all_accesories=c.all_accesories,
                quantity=c.quantity,
                item_total_price=c.total_cost,
                expected_delivery_date=expected_delivery_date).save()
            c.delete()
        Payment.objects.create(user=request.user,
                               order_number=order_id,
                               email=email,
                               total_price=total_amount).save()
        payment_detail = Payment.objects.get(order_number=order_id)
        verified_order_id = payment_detail.payment_id
        verified_order_email = payment_detail.email
        verified_order_number = payment_detail.order_number
        final_amount = total_amount

        param_dict = {
            'MID': 'zVCbHg12338453433430',
            'ORDER_ID': str(verified_order_number),
            'TXN_AMOUNT': str(final_amount),
            'CUST_ID': verified_order_email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        }
        # http://127.0.0.1:8000/
        # eget24.herokuapp.com

        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'mobiles/paytm.html',
                      {'param_dict': param_dict})


def address(request):
    return render(request, 'mobiles/address.html')


def orders(request):
    my_orders = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'mobiles/orders.html', {'my_orders': my_orders})


def mobile(request):
    return render(request, 'mobiles/mobile.html')


def checkout(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for users_cart in cart_product:
            tempamount = (users_cart.quantity *
                          users_cart.all_accesories.price)
            total_amount = total_amount + tempamount
    return render(
        request, 'mobiles/checkout.html', {
            'total_amount': total_amount,
            'cart_items': cart_items,
            'total_item': total_item
        })


@transaction.atomic
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    order_id = request.POST.get('ORDERID')
    txn_id = request.POST.get('TXNID')
    txn_date = request.POST.get('TXNDATE')
    txn_status = request.POST.get('STATUS')
    bank_txn_id = request.POST.get('BANKTXNID')
    resp_msg = request.POST.get('RESPMSG')
    print('THIS IS FORM DATA', form)
    print()
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            filter_data = OrderPlaced.objects.filter(
                order_number=order_id).update(payment_status=str(resp_msg))
            send_order_confirm_message = OrderPlaced.objects.filter(
                order_number=order_id)
            for n in send_order_confirm_message:
                b = n.user.phone_number
            phone_number = b
            my_list = []
            for od in send_order_confirm_message:
                print('ODODODODODO', od)
                print('od', od.all_accesories.title)
                my_list.append(od.all_accesories.title + ' ' + 'quantity :' +
                               str(od.quantity) + ' ' + 'price :' +
                               str(od.item_total_price) + ',')

            def listtostring(my_list):
                str1 = ""
                for ele in my_list:
                    str1 += ele
                return str1

            my_data = listtostring(my_list)
            total_price = Payment.objects.get(order_number=order_id)
            total_amount = total_price.total_price
            # sent_order_confirmation_mesaage(phone_number, my_data,
            # total_amount, order_id, txn_id,
            # txn_date, txn_status, bank_txn_id,
            # resp_msg)

        else:
            print('order was not successful because' +
                  response_dict['RESPMSG'])
            delete_record = OrderPlaced.objects.filter(
                order_number=order_id).delete()
            delete_address = CustomerAddress.objects.filter(
                order_number=order_id).delete()
            delete_Payment_record = Payment.objects.filter(
                order_number=order_id).delete()
    return render(request, 'mobiles/paymentstatus.html',
                  {'response': response_dict})


def search(request):
    query = request.GET.get('search')
    print(query, 'QUERY')
    search_results = All_Accesories.objects.filter(
        title=query) or All_Accesories.objects.filter(
            description=query) or All_Accesories.objects.filter(
                all_mobiles__mobile_name=query
            ) or All_Accesories.objects.filter(
                description=query) or All_Accesories.objects.filter(
                    all_mobiles__all_brands__brand_name=query)
    return render(request, 'mobiles/search-product.html', {
        'search_results': search_results,
        'query': query
    })


def return_order(request, id):
    order = OrderPlaced.objects.get(id=id)
    return_requestt = Return_Order.objects.filter(order_placed=order)
    if return_requestt:
        for i in return_requestt:
            print('THIS IS RETURN REQUEST', i.return_request)
            print(i.return_request)
            print(i.return_status)
    else:
        print('no order found')

    delevery_date = order.expected_delivery_date
    date_format = parse(delevery_date)
    format_delevery_date = date_format.date()
    todays_date = datetime.date.today()
    result_date = todays_date - format_delevery_date
    total_days = result_date.days
    print(total_days)
    print(type(total_days))
    if total_days > 15:
        #  messages.success(
        #             request,
        #             'sorry!! you can not return this orer now')
        pass
    return render(request, 'mobiles/orders.html')
