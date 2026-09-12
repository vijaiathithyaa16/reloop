import React from 'react';
import {
  Send,
  QrCode,
  ExternalLink,
  X,
  CheckCircle2,
  MessageCircle,
  MapPin
} from 'lucide-react';
import { QRCodeSVG } from '../common/QRCodeSVG';

interface TelegramRedirectorModalProps {
  isOpen: boolean;
  onClose: () => void;
}

// Replace with your bot's real @username from BotFather.
// The ?start=reloop_web payload tags pickups that came from this website
// so they're distinguishable from QR-code or direct entries in analytics.
const TELEGRAM_BOT_USERNAME = 'Re_LoopBot';
const TELEGRAM_DEEP_LINK = `https://t.me/${TELEGRAM_BOT_USERNAME}?start=reloop_web`;

export const TelegramRedirectorModal: React.FC<TelegramRedirectorModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div
      id="telegram-redirector-modal-backdrop"
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-900/75 backdrop-blur-xs animate-in fade-in"
    >
      <div
        id="telegram-redirector-modal-container"
        className="max-w-md w-full bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[92vh]"
      >
        <div className="p-5 sm:p-6 flex flex-col overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between mb-3">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-sky-100 text-sky-800 rounded-full text-xs font-bold">
              <Send className="w-3.5 h-3.5 text-sky-600" />
              <span>Live Telegram Bot</span>
            </div>
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-slate-600 text-lg font-bold p-1"
              aria-label="Close"
            >
              ✕
            </button>
          </div>

          <h3 className="text-xl font-extrabold text-slate-900 font-display">
            Scan & Chat on Telegram
          </h3>
          <p className="text-xs text-slate-600 mt-1 leading-relaxed">
            Point your phone's camera at this QR code, or tap the button below on mobile.
            Our bot will collect your item details, verify a photo with AI, take your pickup
            location, and connect you with your nearest collector.
          </p>

          {/* QR Code */}
          <div className="mt-4 p-4 bg-white rounded-2xl border border-slate-200 shadow-xs text-center">
            <div className="flex justify-center">
              <QRCodeSVG value={TELEGRAM_DEEP_LINK} size={170} showValueLabel={false} />
            </div>
            <div className="mt-2.5 flex items-center justify-center gap-1.5 text-sky-700 text-xs font-bold">
              <CheckCircle2 className="w-3.5 h-3.5 text-sky-600 shrink-0" />
              <span>Standard Scannable ISO QR Code</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Opens the ReLoop bot directly in the Telegram app.
            </p>
          </div>

          {/* What happens next */}
          <div className="mt-4 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-2">
            <div className="flex items-start gap-2">
              <MessageCircle className="w-3.5 h-3.5 text-sky-600 shrink-0 mt-0.5" />
              <span>Describe your e-waste and upload a photo for instant AI verification.</span>
            </div>
            <div className="flex items-start gap-2">
              <MapPin className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
              <span>
                Share your location — we'll match you with the nearest collector and hand you
                off to <strong>their WhatsApp</strong> to confirm the pickup.
              </span>
            </div>
          </div>

          {/* Action Links */}
          <div className="mt-4 pt-3 border-t border-slate-200 space-y-2">
            <a
              href={TELEGRAM_DEEP_LINK}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-sky-600 hover:bg-sky-700 text-white font-bold rounded-xl text-xs shadow-xs transition-colors cursor-pointer"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              <span>Open in Telegram</span>
            </a>
            <div className="flex items-center justify-center text-[11px] text-slate-500">
              <span>Bengaluru Official • CPCB</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
